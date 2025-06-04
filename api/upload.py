from http.server import BaseHTTPRequestHandler
import json
import os
import base64
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
        files = body.get('files', [])
        
        if not files:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Nenhum arquivo enviado'})
            }
        
        # Processar cada arquivo
        processed_files = []
        session_data = {}
        validation_errors = []
        
        for file in files:
            filename = file.get('name', '')
            content = file.get('content', '')
            
            if not filename or not content:
                validation_errors.append(f"Arquivo inválido: nome ou conteúdo ausente")
                continue
            
            # Decodificar conteúdo base64
            try:
                decoded_content = base64.b64decode(content).decode('utf-8')
            except:
                validation_errors.append(f"Erro ao decodificar o arquivo {filename}: formato inválido")
                continue
            
            # Validar e processar CSV
            validation_result = CSVProcessor.validate_csv(decoded_content)
            
            if validation_result['is_valid']:
                # Processar CSV válido
                csv_data = validation_result['csv_data']
                
                # Calcular métricas para prévia
                store_name = filename.split('.')[0]  # Usar nome do arquivo como nome da loja
                metrics = CSVProcessor.calculate_metrics(csv_data, store_name)
                
                # Obter prévia
                preview = CSVProcessor.get_preview(csv_data)
                
                # Armazenar dados da sessão
                session_data[store_name] = decoded_content
                
                processed_files.append({
                    'filename': filename,
                    'rows': csv_data['row_count'],
                    'columns': csv_data['column_count'],
                    'column_names': csv_data['header'],
                    'preview': preview['rows'],
                    'metrics_preview': {
                        'categorias_populares': metrics.get('categorias_populares', ''),
                        'produtos_mais_vendidos': metrics.get('produtos_mais_vendidos', ''),
                        'produtos_menos_vendidos': metrics.get('produtos_menos_vendidos', '')
                    },
                    'status': 'success',
                    'message': 'Arquivo processado com sucesso'
                })
            else:
                # Arquivo inválido
                validation_errors.append(f"Erro no arquivo {filename}: {validation_result['error']}")
                processed_files.append({
                    'filename': filename,
                    'status': 'error',
                    'message': validation_result['error']
                })
        
        # Verificar se pelo menos um arquivo foi processado com sucesso
        if not any(file.get('status') == 'success' for file in processed_files):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'success': False,
                    'message': 'Nenhum arquivo foi processado com sucesso',
                    'errors': validation_errors,
                    'files': processed_files
                })
            }
        
        # Retornar resultados
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'message': f'{len([f for f in processed_files if f.get("status") == "success"])} arquivo(s) processado(s) com sucesso',
                'warnings': validation_errors if validation_errors else None,
                'files': processed_files,
                'session_data': session_data
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Erro ao processar arquivos: {str(e)}'})
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
