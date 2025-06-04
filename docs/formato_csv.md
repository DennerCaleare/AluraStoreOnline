# Formato Padrão dos Arquivos CSV

Este documento descreve o formato padrão esperado para os arquivos CSV utilizados no Alura Store Analyzer.

## Estrutura Básica

Os arquivos CSV devem seguir estas regras:

1. **Delimitador**: Vírgula (`,`) ou ponto-e-vírgula (`;`)
2. **Codificação**: UTF-8
3. **Cabeçalho**: Obrigatório na primeira linha
4. **Nomes dos arquivos**: Recomenda-se usar o nome da loja como nome do arquivo (ex: `loja_1.csv`, `loja_2.csv`)

## Colunas Obrigatórias

Os arquivos CSV devem conter as seguintes colunas (os nomes são flexíveis e case-insensitive):

| Coluna | Descrição | Formato | Exemplo |
|--------|-----------|---------|---------|
| **Produto** | Nome do produto vendido | Texto | Micro-ondas |
| **Categoria do Produto** | Categoria à qual o produto pertence | Texto | Eletrodomésticos |
| **Preço** | Valor do produto | Numérico (ponto ou vírgula como separador decimal) | 1009.99 ou 1009,99 |
| **Frete** | Valor do frete | Numérico (ponto ou vírgula como separador decimal) | 54.67 ou 54,67 |
| **Data da Compra** | Data em que a compra foi realizada | Data (DD/MM/AAAA) | 03/05/2022 |
| **Avaliação da compra** | Nota dada pelo cliente | Numérico (1-5) | 4 |

## Exemplo de Arquivo CSV Válido

```csv
Produto,Categoria do Produto,Preço,Frete,Data da Compra,Avaliação da compra
Micro-ondas,Eletrodomésticos,1009.99,54.67,03/05/2022,4
TV Led UHD 4K,Eletrônicos,3969.38,216.71,12/02/2020,5
Smartphone,Eletrônicos,2500.00,0.00,15/03/2022,3
Geladeira,Eletrodomésticos,3200.50,120.30,22/04/2022,4
Notebook,Informática,4500.00,35.90,10/01/2022,5
Mouse sem fio,Informática,89.90,12.50,05/02/2022,2
```

## Observações Importantes

1. **Valores numéricos**: Podem usar ponto (`.`) ou vírgula (`,`) como separador decimal
2. **Datas**: Devem estar no formato DD/MM/AAAA
3. **Avaliações**: Devem ser valores numéricos entre 1 e 5
4. **Valores ausentes**: Evite deixar células vazias, especialmente nas colunas obrigatórias
5. **Caracteres especiais**: Evite usar aspas (") dentro dos campos de texto

## Validação Automática

O sistema realiza automaticamente as seguintes validações:

1. Verifica se todas as colunas obrigatórias estão presentes
2. Converte automaticamente valores numéricos com vírgula para ponto decimal
3. Identifica o delimitador correto (vírgula ou ponto-e-vírgula)
4. Verifica se há dados suficientes para análise (mínimo de 3 linhas além do cabeçalho)

## Solução de Problemas

Se o sistema não conseguir processar seu arquivo CSV, verifique:

1. Se o arquivo está no formato CSV correto
2. Se todas as colunas obrigatórias estão presentes
3. Se os valores numéricos estão formatados corretamente
4. Se não há linhas vazias ou corrompidas
5. Se a codificação do arquivo é UTF-8

## Exemplo de Arquivo para Download

Você pode baixar um [arquivo CSV de exemplo aqui](exemplo_loja.csv) para usar como modelo.
