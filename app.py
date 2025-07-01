from flask import Flask, send_from_directory, request, jsonify
import json
import os
import sys

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.csv_processor import CSVProcessor

app = Flask(__name__)

# Servir arquivos estáticos da pasta public
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

# API endpoints
@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        session_data = data.get('session_data', {})
        metrics = data.get('metrics', [])
        
        if not session_data:
            return jsonify({'error': 'Nenhum dado de sessão fornecido'}), 400
        
        if not metrics:
            return jsonify({'error': 'Nenhuma métrica selecionada'}), 400
        
        # Processar dados de cada loja
        store_data = {}
        for store_name, csv_content in session_data.items():
            # Processar CSV
            csv_data = CSVProcessor.parse_csv(csv_content)
            
            # Calcular métricas
            store_metrics = CSVProcessor.calculate_metrics(csv_data, store_name)
            store_data[store_name] = store_metrics
        
        # Calcular pontuações com base nas métricas selecionadas
        scores = {}
        metric_details = []
        
        # Processar cada métrica selecionada
        for metric in metrics:
            metric_id = metric['id']
            metric_name = metric['name']
            metric_weight = metric['weight']
            
            # Coletar valores para esta métrica de todas as lojas
            metric_values = []
            for store_name, store_metrics in store_data.items():
                value = store_metrics.get(metric_id, 0)
                metric_values.append({
                    'store': store_name,
                    'value': value,
                    'details': store_metrics.get(f'{metric_id}_detalhes', [])
                })
            
            # Adicionar detalhes da métrica
            metric_details.append({
                'id': metric_id,
                'name': metric_name,
                'weight': metric_weight,
                'values': metric_values
            })
            
            # Calcular pontuação para cada loja com base nesta métrica
            for store_name in store_data.keys():
                if store_name not in scores:
                    scores[store_name] = 0
                
                # Obter valor da métrica para esta loja
                store_value = next((v['value'] for v in metric_values if v['store'] == store_name), 0)
                
                # Calcular pontuação com base no tipo de métrica
                score = 0
                
                if metric_id == 'faturamento_total':
                    # Maior faturamento = melhor pontuação
                    max_value = max([v['value'] for v in metric_values]) if metric_values else 0
                    min_value = min([v['value'] for v in metric_values]) if metric_values else 0
                    range_value = max_value - min_value
                    
                    if range_value > 0:
                        score = ((store_value - min_value) / range_value) * 10
                    else:
                        score = 5  # Valor padrão se todas as lojas tiverem o mesmo faturamento
                
                elif metric_id == 'media_avaliacao':
                    # Maior avaliação = melhor pontuação (escala 1-5 para 0-10)
                    score = ((store_value - 1) / 4) * 10 if store_value > 0 else 0
                
                elif metric_id == 'custo_medio_frete':
                    # Menor frete = melhor pontuação (invertido)
                    max_value = max([v['value'] for v in metric_values]) if metric_values else 0
                    min_value = min([v['value'] for v in metric_values]) if metric_values else 0
                    range_value = max_value - min_value
                    
                    if range_value > 0:
                        score = 10 - (((store_value - min_value) / range_value) * 10)
                    else:
                        score = 5  # Valor padrão se todas as lojas tiverem o mesmo frete
                
                else:
                    # Para outras métricas, usar pontuação padrão
                    score = 5
                
                # Aplicar peso da métrica
                scores[store_name] += score * metric_weight
        
        # Ordenar lojas por pontuação (decrescente - maior pontuação é melhor)
        sorted_stores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Preparar resultados
        results = {
            'recommendedStore': sorted_stores[0][0],
            'storeRankings': [
                {
                    'name': store[0],
                    'score': round(store[1], 2),
                    'rank': idx + 1
                } for idx, store in enumerate(sorted_stores)
            ],
            'metricDetails': metric_details
        }
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao analisar dados: {str(e)}'}), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    try:
        # Simular upload - na verdade apenas validar o conteúdo CSV
        files = request.files
        results = {}
        
        for file_key in files:
            file = files[file_key]
            if file and file.filename:
                content = file.read().decode('utf-8')
                
                # Validar CSV
                try:
                    csv_data = CSVProcessor.parse_csv(content)
                    results[file.filename] = {
                        'success': True,
                        'content': content,
                        'rows': len(csv_data)
                    }
                except Exception as e:
                    results[file.filename] = {
                        'success': False,
                        'error': str(e)
                    }
        
        return jsonify({
            'success': True,
            'files': results
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro no upload: {str(e)}'}), 500

@app.route('/api/export_pdf', methods=['POST'])
def export_pdf():
    try:
        data = request.get_json()
        # Simular exportação de PDF
        return jsonify({
            'success': True,
            'message': 'PDF gerado com sucesso',
            'download_url': '/api/download_pdf'
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao exportar PDF: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

