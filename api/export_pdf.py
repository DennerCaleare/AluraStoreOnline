from http.server import BaseHTTPRequestHandler
import json
import os
from utils.csv_processor import CSVProcessor
import base64
from weasyprint import HTML, CSS
from datetime import datetime
import tempfile

def generate_pdf_report(analysis_results, store_data):
    """
    Gera um relatório em PDF com os resultados da análise
    """
    # Criar HTML para o relatório
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Análise - Alura Store</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: "Noto Sans CJK SC", "WenQuanYi Zen Hei", sans-serif;
                line-height: 1.5;
                color: #333;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
            }}
            .header h1 {{
                color: #7c4dff;
                margin-bottom: 5px;
            }}
            .header p {{
                color: #666;
                margin-top: 0;
            }}
            .recommendation {{
                background-color: #f1f8ff;
                border-left: 4px solid #7c4dff;
                padding: 15px;
                margin: 20px 0;
            }}
            .recommendation h2 {{
                margin-top: 0;
                color: #7c4dff;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: left;
            }}
            th {{
                background-color: #f5f5f5;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .metric-section {{
                margin: 30px 0;
            }}
            .metric-section h3 {{
                color: #7c4dff;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }}
            .chart-container {{
                width: 100%;
                height: 300px;
                margin: 20px 0;
                text-align: center;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 0.8em;
                color: #666;
                border-top: 1px solid #ddd;
                padding-top: 10px;
            }}
            .progress-bar {{
                height: 20px;
                background-color: #e9ecef;
                border-radius: 10px;
                margin-bottom: 10px;
                overflow: hidden;
            }}
            .progress-bar-fill {{
                height: 100%;
                background-color: #7c4dff;
                border-radius: 10px;
            }}
            .store-card {{
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
            }}
            .store-header {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }}
            .store-name {{
                font-weight: bold;
                font-size: 1.2em;
            }}
            .store-score {{
                font-weight: bold;
            }}
            .metric-value {{
                font-weight: bold;
                color: #7c4dff;
            }}
            .chart-placeholder {{
                width: 100%;
                height: 200px;
                background-color: #f5f5f5;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #666;
                border: 1px dashed #ccc;
            }}
            .badge {{
                display: inline-block;
                padding: 3px 8px;
                background-color: #f1f1f1;
                border-radius: 10px;
                margin-right: 5px;
                margin-bottom: 5px;
                font-size: 0.9em;
            }}
            .badge-count {{
                background-color: #7c4dff;
                color: white;
                border-radius: 10px;
                padding: 2px 6px;
                font-size: 0.8em;
                margin-left: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Relatório de Análise - Alura Store</h1>
            <p>Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
        </div>
        
        <div class="recommendation">
            <h2>Recomendação</h2>
            <p>Com base na análise das métricas selecionadas, recomendamos vender a <strong>{analysis_results['recommendedStore']}</strong>.</p>
        </div>
        
        <div class="metric-section">
            <h3>Ranking das Lojas</h3>
            
            <div class="store-rankings">
    """
    
    # Adicionar ranking das lojas
    for store in analysis_results['storeRankings']:
        store_name = store['name']
        store_score = store['score']
        store_rank = store['rank']
        max_score = max([s['score'] for s in analysis_results['storeRankings']])
        percentage = (store_score / max_score) * 100
        
        html_content += f"""
                <div class="store-card">
                    <div class="store-header">
                        <div class="store-name">{store_name}</div>
                        <div class="store-score">{store_score:.1f} pontos</div>
                    </div>
                    <div>Ranking #{store_rank}</div>
                    <div class="progress-bar">
                        <div class="progress-bar-fill" style="width: {percentage}%;"></div>
                    </div>
                </div>
        """
    
    html_content += """
            </div>
        </div>
        
        <div class="metric-section">
            <h3>Detalhes por Métrica</h3>
    """
    
    # Adicionar detalhes por métrica
    for metric in analysis_results['metricDetails']:
        metric_name = metric['name']
        metric_weight = metric['weight']
        
        html_content += f"""
            <div class="metric-section">
                <h4>{metric_name} <small>(Peso: {metric_weight})</small></h4>
        """
        
        # Verificar se é uma métrica especial (categorias ou produtos)
        if metric_name.lower() in ['categorias populares', 'produtos mais vendidos', 'produtos menos vendidos']:
            html_content += """
                <div>
            """
            
            for value in metric['values']:
                store = value['store']
                html_content += f"""
                    <h5>{store}</h5>
                    <div>
                """
                
                if 'details' in value and value['details']:
                    for detail in value['details']:
                        item_name = detail.get('categoria', detail.get('produto', ''))
                        count = detail.get('contagem', 0)
                        percentage = detail.get('porcentagem', 0)
                        
                        html_content += f"""
                        <span class="badge">{item_name} <span class="badge-count">{count}</span> ({percentage}%)</span>
                        """
                
                html_content += """
                    </div>
                """
            
            html_content += """
                </div>
            """
        else:
            # Para métricas numéricas, usar tabela
            html_content += """
                <table>
                    <thead>
                        <tr>
                            <th>Loja</th>
                            <th>Valor</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for value in metric['values']:
                store = value['store']
                val = value['value']
                
                if isinstance(val, (int, float)):
                    formatted_val = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                else:
                    formatted_val = val
                
                html_content += f"""
                        <tr>
                            <td>{store}</td>
                            <td class="metric-value">{formatted_val}</td>
                        </tr>
                """
            
            html_content += """
                    </tbody>
                </table>
            """
        
        html_content += """
            </div>
        """
    
    # Adicionar estatísticas gerais
    html_content += """
        <div class="metric-section">
            <h3>Estatísticas Gerais</h3>
            <table>
                <thead>
                    <tr>
                        <th>Loja</th>
                        <th>Total de Produtos</th>
                        <th>Categorias Únicas</th>
                        <th>Produtos Únicos</th>
                        <th>Faturamento Total</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for store_name, metrics in store_data.items():
        total_produtos = metrics.get('total_produtos', 0)
        total_categorias = metrics.get('total_categorias', 0)
        total_produtos_unicos = metrics.get('total_produtos_unicos', 0)
        faturamento = metrics.get('faturamento_total', 0)
        
        html_content += f"""
                    <tr>
                        <td>{store_name}</td>
                        <td>{total_produtos}</td>
                        <td>{total_categorias}</td>
                        <td>{total_produtos_unicos}</td>
                        <td>R$ {faturamento:,.2f}</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
        </div>
    """
    
    # Finalizar HTML
    html_content += """
        <div class="footer">
            <p>Este relatório foi gerado automaticamente pelo Alura Store Analyzer.</p>
            <p>© 2025 Alura Store Analyzer</p>
        </div>
    </body>
    </html>
    """
    
    # Criar arquivo temporário para o PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        # Gerar PDF com WeasyPrint
        HTML(string=html_content).write_pdf(tmp.name)
        
        # Ler o arquivo PDF gerado
        with open(tmp.name, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # Remover arquivo temporário
        os.unlink(tmp.name)
    
    return pdf_content

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
        analysis_results = body.get('analysis_results', {})
        session_data = body.get('session_data', {})
        
        if not analysis_results or not session_data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Dados insuficientes para gerar o relatório'})
            }
        
        # Processar dados de cada loja para o relatório
        store_data = {}
        for store_name, csv_content in session_data.items():
            # Processar CSV
            csv_data = CSVProcessor.parse_csv(csv_content)
            
            # Calcular métricas
            store_metrics = CSVProcessor.calculate_metrics(csv_data, store_name)
            store_data[store_name] = store_metrics
        
        # Gerar PDF
        pdf_content = generate_pdf_report(analysis_results, store_data)
        
        # Codificar PDF em base64
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
        
        # Retornar PDF
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Content-Disposition': 'attachment; filename="relatorio_alura_store.pdf"'
            },
            'body': json.dumps({
                'success': True,
                'pdf_base64': pdf_base64,
                'filename': 'relatorio_alura_store.pdf'
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Erro ao gerar relatório: {str(e)}'})
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
        for header, value in result.get('headers', {}).items():
            self.send_header(header, value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(result.get('body', '').encode())
        return
