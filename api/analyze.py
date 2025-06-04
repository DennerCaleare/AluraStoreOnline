from http.server import BaseHTTPRequestHandler
import json
import os
from utils.csv_processor import CSVProcessor

def handler(request):
    # Verificar método
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Método não permitido'})
        }
    
    # Obter dados do corpo da requisição
    try:
        body = json.loads(request.body)
        session_data = body.get('session_data', {})
        metrics = body.get('metrics', [])
        
        if not session_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Nenhum dado de sessão fornecido'})
            }
        
        if not metrics:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Nenhuma métrica selecionada'})
            }
        
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
        
        # Ordenar lojas por pontuação (crescente - menor pontuação é pior)
        sorted_stores = sorted(scores.items(), key=lambda x: x[1])
        
        # Preparar resultados
        results = {
            'recommendedStore': sorted_stores[0][0],
            'storeRankings': [
                {
                    'name': store[0],
                    'score': store[1],
                    'rank': idx + 1
                } for idx, store in enumerate(sorted_stores)
            ],
            'metricDetails': metric_details
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'results': results
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Erro ao analisar dados: {str(e)}'})
        }

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Criar objeto de requisição simulado
        request = type('obj', (object,), {
            'method': 'POST',
            'body': post_data
        })
        
        result = handler(request)
        
        self.send_response(result.get('statusCode', 200))
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(result.get('body', '').encode())
        return
