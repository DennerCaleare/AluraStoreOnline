# Alura Store Analyzer - Versão 3.0

## Sobre o Projeto

O Alura Store Analyzer é uma aplicação web interativa desenvolvida para auxiliar na análise de desempenho de lojas com base em dados de vendas. A aplicação permite o upload de múltiplos arquivos CSV contendo dados de vendas de diferentes lojas, a seleção personalizada de métricas de análise e a definição de pesos para cada métrica, gerando recomendações sobre qual loja apresenta o menor desempenho.

**Novidades na versão 3.0:**
- **Processo mais automático** para upload e validação de arquivos CSV
- **Documentação detalhada** sobre o formato esperado dos arquivos CSV
- **Saída mais organizada** com visualização clara dos resultados
- **Exportação de relatório em PDF** com layout moderno e profissional
- Interface de login segura (usuário: admin, senha: admin)
- Análise aprimorada de categorias populares e produtos mais/menos vendidos

## Funcionalidades

- **Autenticação de usuário**: Sistema de login simples para controle de acesso
- **Upload de múltiplos arquivos CSV**: Suporte para carregar dados de várias lojas simultaneamente
- **Validação automática de arquivos**: Verificação do formato e conteúdo dos arquivos CSV
- **Pré-visualização de dados**: Visualização rápida dos dados carregados antes da análise
- **Pré-visualização de métricas**: Visualização das métricas principais diretamente na tela de upload
- **Seleção de métricas personalizadas**: Escolha quais métricas considerar na análise
- **Definição de pesos**: Atribuição de importância relativa para cada métrica
- **Análise dinâmica**: Processamento em tempo real com base nas configurações do usuário
- **Resultados detalhados**: Visualização de rankings, pontuações e detalhes por métrica
- **Exportação em PDF**: Geração de relatórios profissionais em formato PDF
- **Interface responsiva**: Experiência consistente em dispositivos desktop e móveis

## Métricas Disponíveis

- **Faturamento Total**: Soma total do valor das vendas
- **Média de Avaliação**: Média das avaliações dos clientes
- **Categorias Populares**: Análise das categorias mais vendidas com contagens precisas e percentuais
- **Produtos Mais Vendidos**: Análise dos produtos com maior volume de vendas com contagens precisas e percentuais
- **Produtos Menos Vendidos**: Análise dos produtos com menor volume de vendas com contagens precisas e percentuais
- **Custo Médio do Frete**: Média dos valores de frete

## Requisitos

- Python 3.8+
- Flask
- WeasyPrint (para geração de PDF)
- Navegador web moderno

## Instalação e Execução Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/alura-store-analyzer.git
   cd alura-store-analyzer
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   python src/main.py
   ```

5. Acesse a aplicação no navegador:
   ```
   http://localhost:5000
   ```

6. Faça login com as credenciais:
   - Usuário: `admin`
   - Senha: `admin`

## Estrutura do Projeto

```
alura_store_analyzer_vercel/
├── api/                  # Funções serverless para o Vercel
│   ├── upload.py         # Endpoint para upload e validação de arquivos
│   ├── analyze.py        # Endpoint para análise de dados
│   └── export_pdf.py     # Endpoint para exportação de relatórios em PDF
├── docs/                 # Documentação
│   ├── formato_csv.md    # Especificação do formato CSV esperado
│   └── exemplos/         # Arquivos CSV de exemplo
├── public/               # Arquivos estáticos
│   ├── index.html        # Interface principal da aplicação
│   ├── login.html        # Página de login
│   └── css/              # Estilos CSS (embutidos no HTML)
├── utils/                # Utilitários para processamento
│   └── csv_processor.py  # Processamento e validação de CSV
├── requirements.txt      # Dependências Python
├── vercel.json           # Configuração do Vercel
└── README.md             # Este guia
```

## Guia de Uso

### 1. Login

1. Acesse a aplicação através da URL fornecida
2. Na tela de login, insira as credenciais:
   - Usuário: `admin`
   - Senha: `admin`
3. Clique em "Entrar" para acessar a aplicação

### 2. Upload de Arquivos

1. Na tela inicial, arraste e solte arquivos CSV ou clique em "Selecionar Arquivos"
2. Os arquivos devem seguir o formato padrão documentado (clique em "Ver formato esperado" para detalhes)
3. O sistema validará automaticamente os arquivos e exibirá mensagens de erro se necessário
4. Após o upload bem-sucedido, você pode:
   - Visualizar os dados clicando no ícone de olho
   - Ver uma prévia das métricas clicando no ícone de gráfico
5. Clique em "Continuar para Métricas" para prosseguir

### 3. Configuração de Métricas

1. Selecione as métricas que deseja incluir na análise (todas são selecionadas por padrão)
2. Ajuste os pesos de cada métrica usando os controles deslizantes (1-10)
3. Clique em "Analisar Dados" para prosseguir

### 4. Resultados

1. Visualize a recomendação principal sobre qual loja vender
2. Explore o ranking completo das lojas com suas pontuações
3. Analise os detalhes por métrica para entender os fatores que influenciaram a decisão
4. Clique em "Exportar Relatório PDF" para gerar um relatório profissional
5. Use o botão "Nova Análise" para recomeçar o processo ou "Voltar" para ajustar as métricas
6. Para sair da aplicação, clique no ícone de usuário no canto superior direito e selecione "Sair"

## Formato dos Arquivos CSV

Os arquivos CSV devem seguir um formato específico para serem processados corretamente. Consulte a documentação detalhada em [docs/formato_csv.md](docs/formato_csv.md) para mais informações.

Um arquivo de exemplo está disponível em [docs/exemplos/exemplo_loja.csv](docs/exemplos/exemplo_loja.csv).

## Personalização e Extensão

### Alterando as Credenciais de Login

Para alterar as credenciais de login padrão (admin/admin):

1. Abra o arquivo `public/login.html`
2. Localize a função de verificação de credenciais (aproximadamente linha 100)
3. Modifique os valores de usuário e senha conforme desejado

### Adicionando Novas Métricas

Para adicionar novas métricas à análise:

1. Modifique o arquivo `utils/csv_processor.py` para incluir a nova métrica na função `calculate_metrics`
2. Atualize a função `handler` em `api/analyze.py` para calcular a nova métrica
3. Adicione a nova métrica à lista `availableMetrics` no arquivo `public/index.html`

### Personalizando o Relatório PDF

Para personalizar o layout do relatório PDF:

1. Modifique o arquivo `api/export_pdf.py`
2. Atualize o HTML e CSS na função `generate_pdf_report`
3. Adicione novos elementos ou seções conforme necessário

## Implantação no Vercel

Para implantar no Vercel, siga as instruções detalhadas no arquivo `IMPLANTACAO.md`.

## Solução de Problemas

### Erro ao fazer login

- Verifique se está usando as credenciais corretas (admin/admin por padrão)
- Limpe o cache do navegador e tente novamente
- Verifique se o JavaScript está habilitado no navegador

### Erro ao fazer upload de arquivos

- Verifique se os arquivos estão no formato CSV correto (consulte docs/formato_csv.md)
- Confirme que o separador é vírgula (,) ou ponto e vírgula (;)
- Verifique se as colunas necessárias estão presentes
- Observe as mensagens de erro exibidas pelo sistema para orientação específica

### Erro ao exportar PDF

- Verifique se o navegador permite downloads automáticos
- Tente novamente após alguns segundos, pois a geração do PDF pode levar tempo
- Se o problema persistir, tente usar outro navegador

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
