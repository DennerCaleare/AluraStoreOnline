from http.server import BaseHTTPRequestHandler
import json
import os
import csv
import io
import base64
from urllib.parse import parse_qs

class CSVProcessor:
    @staticmethod
    def parse_csv(csv_content, delimiter=','):
        """
        Processa o conteúdo de um arquivo CSV
        """
        try:
            # Tenta com o delimitador fornecido
            csv_file = io.StringIO(csv_content)
            reader = csv.reader(csv_file, delimiter=delimiter)
            
            # Lê o cabeçalho
            header = next(reader)
            
            # Se o cabeçalho tem apenas uma coluna, tenta outro delimitador
            if len(header) <= 1 and delimiter == ',':
                return CSVProcessor.parse_csv(csv_content, ';')
            
            # Lê os dados
            rows = list(reader)
            
            return {
                'header': header,
                'rows': rows,
                'row_count': len(rows),
                'column_count': len(header)
            }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    @staticmethod
    def validate_csv(csv_content):
        """
        Valida o conteúdo de um arquivo CSV
        """
        # Verificar se o conteúdo está vazio
        if not csv_content or len(csv_content.strip()) == 0:
            return {
                'is_valid': False,
                'error': 'O arquivo está vazio'
            }
        
        # Tentar processar o CSV
        csv_data = CSVProcessor.parse_csv(csv_content)
        
        # Verificar se houve erro no processamento
        if 'error' in csv_data:
            return {
                'is_valid': False,
                'error': f'Erro ao processar o CSV: {csv_data["error"]}'
            }
        
        # Verificar se há dados suficientes
        if csv_data['row_count'] < 3:
            return {
                'is_valid': False,
                'error': 'O arquivo deve conter pelo menos 3 linhas de dados além do cabeçalho'
            }
        
        # Verificar colunas obrigatórias
        required_columns = ['produto', 'categoria', 'preço', 'frete', 'data', 'avaliação']
        header_lower = [col.lower() for col in csv_data['header']]
        
        missing_columns = []
        for req_col in required_columns:
            if not any(req_col in col for col in header_lower):
                missing_columns.append(req_col)
        
        if missing_columns:
            return {
                'is_valid': False,
                'error': f'Colunas obrigatórias ausentes: {", ".join(missing_columns)}'
            }
        
        # Verificar valores numéricos nas colunas de preço, frete e avaliação
        price_col = next((i for i, col in enumerate(header_lower) if 'preço' in col), -1)
        shipping_col = next((i for i, col in enumerate(header_lower) if 'frete' in col), -1)
        rating_col = next((i for i, col in enumerate(header_lower) if 'avaliação' in col), -1)
        
        for i, row in enumerate(csv_data['rows']):
            if len(row) < len(csv_data['header']):
                return {
                    'is_valid': False,
                    'error': f'Linha {i+2} tem menos colunas que o cabeçalho'
                }
            
            # Verificar preço
            if price_col >= 0:
                try:
                    float(row[price_col].replace(',', '.'))
                except:
                    return {
                        'is_valid': False,
                        'error': f'Valor de preço inválido na linha {i+2}: {row[price_col]}'
                    }
            
            # Verificar frete
            if shipping_col >= 0:
                try:
                    float(row[shipping_col].replace(',', '.'))
                except:
                    return {
                        'is_valid': False,
                        'error': f'Valor de frete inválido na linha {i+2}: {row[shipping_col]}'
                    }
            
            # Verificar avaliação
            if rating_col >= 0:
                try:
                    rating = float(row[rating_col].replace(',', '.'))
                    if rating < 1 or rating > 5:
                        return {
                            'is_valid': False,
                            'error': f'Avaliação deve estar entre 1 e 5 na linha {i+2}: {row[rating_col]}'
                        }
                except:
                    return {
                        'is_valid': False,
                        'error': f'Valor de avaliação inválido na linha {i+2}: {row[rating_col]}'
                    }
        
        # Se chegou até aqui, o CSV é válido
        return {
            'is_valid': True,
            'csv_data': csv_data
        }
    
    @staticmethod
    def get_preview(csv_data, max_rows=5):
        """
        Obtém uma prévia dos dados CSV
        """
        if 'error' in csv_data:
            return csv_data
        
        preview = {
            'header': csv_data['header'],
            'rows': csv_data['rows'][:max_rows],
            'row_count': csv_data['row_count'],
            'column_count': csv_data['column_count']
        }
        
        return preview
    
    @staticmethod
    def extract_column_data(csv_data, column_name):
        """
        Extrai dados de uma coluna específica
        """
        if 'error' in csv_data:
            return []
        
        try:
            column_index = csv_data['header'].index(column_name)
            return [row[column_index] for row in csv_data['rows'] if len(row) > column_index]
        except ValueError:
            return []
        except Exception as e:
            return []
    
    @staticmethod
    def calculate_metrics(csv_data, store_name):
        """
        Calcula métricas detalhadas para uma loja
        """
        metrics = {}
        
        # Verificar se há dados válidos
        if 'error' in csv_data or not csv_data.get('rows'):
            return {'error': 'Dados inválidos ou insuficientes'}
        
        header = csv_data['header']
        rows = csv_data['rows']
        
        # Mapear índices de colunas importantes
        column_indices = {}
        important_columns = ['Produto', 'Categoria do Produto', 'Preço', 'Frete', 'Avaliação da compra']
        
        for col in important_columns:
            try:
                # Busca exata
                if col in header:
                    column_indices[col] = header.index(col)
                else:
                    # Busca parcial (case insensitive)
                    for i, h in enumerate(header):
                        if col.lower().split()[0] in h.lower():
                            column_indices[col] = i
                            break
            except ValueError:
                # Coluna não encontrada
                pass
        
        # 1. Faturamento Total
        if 'Preço' in column_indices:
            try:
                prices = []
                for row in rows:
                    if len(row) > column_indices['Preço'] and row[column_indices['Preço']].strip():
                        price_str = row[column_indices['Preço']].replace(',', '.')
                        prices.append(float(price_str))
                
                metrics['faturamento_total'] = sum(prices)
            except Exception as e:
                metrics['faturamento_total'] = 0
                metrics['error_faturamento'] = str(e)
        
        # 2. Média de Avaliação
        if 'Avaliação da compra' in column_indices:
            try:
                ratings = []
                for row in rows:
                    if len(row) > column_indices['Avaliação da compra'] and row[column_indices['Avaliação da compra']].strip():
                        rating_str = row[column_indices['Avaliação da compra']].replace(',', '.')
                        ratings.append(float(rating_str))
                
                metrics['media_avaliacao'] = sum(ratings) / len(ratings) if ratings else 0
            except Exception as e:
                metrics['media_avaliacao'] = 0
                metrics['error_avaliacao'] = str(e)
        
        # 3. Custo Médio do Frete
        if 'Frete' in column_indices:
            try:
                shipping_costs = []
                for row in rows:
                    if len(row) > column_indices['Frete'] and row[column_indices['Frete']].strip():
                        cost_str = row[column_indices['Frete']].replace(',', '.')
                        shipping_costs.append(float(cost_str))
                
                metrics['custo_medio_frete'] = sum(shipping_costs) / len(shipping_costs) if shipping_costs else 0
            except Exception as e:
                metrics['custo_medio_frete'] = 0
                metrics['error_frete'] = str(e)
        
        # 4. Categorias Populares
        if 'Categoria do Produto' in column_indices:
            try:
                categories = {}
                for row in rows:
                    if len(row) > column_indices['Categoria do Produto'] and row[column_indices['Categoria do Produto']].strip():
                        category = row[column_indices['Categoria do Produto']].strip()
                        categories[category] = categories.get(category, 0) + 1
                
                # Ordenar por contagem (decrescente)
                sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
                top_categories = sorted_categories[:5]
                
                metrics['categorias_populares'] = ', '.join([cat[0] for cat in top_categories])
                metrics['categorias_populares_counts'] = {cat[0]: cat[1] for cat in top_categories}
                metrics['categorias_populares_detalhes'] = [{"categoria": cat[0], "contagem": cat[1], "porcentagem": round(cat[1] / len(rows) * 100, 1)} for cat in top_categories]
                
                # Calcular distribuição percentual
                total_items = sum(categories.values())
                metrics['categorias_distribuicao'] = [
                    {
                        "categoria": cat[0],
                        "contagem": cat[1],
                        "porcentagem": round(cat[1] / total_items * 100, 1)
                    } for cat in sorted_categories
                ]
            except Exception as e:
                metrics['categorias_populares'] = ''
                metrics['categorias_populares_counts'] = {}
                metrics['error_categorias'] = str(e)
        
        # 5. Produtos Mais Vendidos
        if 'Produto' in column_indices:
            try:
                products = {}
                for row in rows:
                    if len(row) > column_indices['Produto'] and row[column_indices['Produto']].strip():
                        product = row[column_indices['Produto']].strip()
                        products[product] = products.get(product, 0) + 1
                
                # Ordenar por contagem (decrescente)
                sorted_products = sorted(products.items(), key=lambda x: x[1], reverse=True)
                top_products = sorted_products[:5]
                
                metrics['produtos_mais_vendidos'] = ', '.join([prod[0] for prod in top_products])
                metrics['produtos_mais_vendidos_counts'] = {prod[0]: prod[1] for prod in top_products}
                metrics['produtos_mais_vendidos_detalhes'] = [{"produto": prod[0], "contagem": prod[1], "porcentagem": round(prod[1] / len(rows) * 100, 1)} for prod in top_products]
                
                # 6. Produtos Menos Vendidos
                if len(sorted_products) >= 5:
                    bottom_products = sorted_products[-5:]
                    bottom_products.reverse()  # Inverter para mostrar do menos vendido para o mais vendido
                    metrics['produtos_menos_vendidos'] = ', '.join([prod[0] for prod in bottom_products])
                    metrics['produtos_menos_vendidos_counts'] = {prod[0]: prod[1] for prod in bottom_products}
                    metrics['produtos_menos_vendidos_detalhes'] = [{"produto": prod[0], "contagem": prod[1], "porcentagem": round(prod[1] / len(rows) * 100, 1)} for prod in bottom_products]
                else:
                    metrics['produtos_menos_vendidos'] = 'Dados insuficientes'
                    metrics['produtos_menos_vendidos_counts'] = {}
                    metrics['produtos_menos_vendidos_detalhes'] = []
            except Exception as e:
                metrics['produtos_mais_vendidos'] = ''
                metrics['produtos_mais_vendidos_counts'] = {}
                metrics['produtos_menos_vendidos'] = ''
                metrics['produtos_menos_vendidos_counts'] = {}
                metrics['error_produtos'] = str(e)
        
        # 7. Estatísticas gerais
        metrics['total_produtos'] = len(rows)
        metrics['total_categorias'] = len(categories) if 'categories' in locals() else 0
        metrics['total_produtos_unicos'] = len(products) if 'products' in locals() else 0
        
        # 8. Dados para gráficos
        if 'Preço' in column_indices and 'Avaliação da compra' in column_indices:
            try:
                price_rating_data = []
                for row in rows:
                    if (len(row) > column_indices['Preço'] and row[column_indices['Preço']].strip() and
                        len(row) > column_indices['Avaliação da compra'] and row[column_indices['Avaliação da compra']].strip()):
                        price = float(row[column_indices['Preço']].replace(',', '.'))
                        rating = float(row[column_indices['Avaliação da compra']].replace(',', '.'))
                        price_rating_data.append({"preco": price, "avaliacao": rating})
                
                metrics['price_rating_data'] = price_rating_data[:100]  # Limitar a 100 pontos para o gráfico
            except Exception as e:
                metrics['price_rating_data'] = []
        
        return metrics
