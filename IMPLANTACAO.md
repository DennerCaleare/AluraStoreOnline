# Guia de Implantação no Vercel - Passo a Passo

Este documento fornece instruções detalhadas para implantar o Alura Store Analyzer no Vercel, com foco em usuários que estão fazendo isso pela primeira vez.

## Pré-requisitos

1. Uma conta no Vercel (gratuita)
2. Git instalado em seu computador (opcional, mas recomendado)
3. Node.js instalado (opcional, apenas para desenvolvimento local)

## Passo 1: Preparar o Código

1. Descompacte o arquivo ZIP que você recebeu em uma pasta em seu computador
2. Verifique se a estrutura de pastas está correta:
   ```
   alura_store_analyzer_vercel/
   ├── api/
   ├── public/
   ├── utils/
   ├── requirements.txt
   ├── vercel.json
   └── README.md
   ```

## Passo 2: Criar uma Conta no Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Clique em "Sign Up" e crie uma conta usando GitHub, GitLab, Bitbucket ou e-mail
3. Complete o processo de registro

## Passo 3: Implantar o Projeto

### Opção A: Usando o Dashboard do Vercel (Mais Fácil)

1. Faça login no [dashboard do Vercel](https://vercel.com/dashboard)
2. Clique no botão "Add New..." e selecione "Project"
3. Na seção "Import Git Repository", clique em "Upload" (na parte inferior da tela)
4. Arraste a pasta `alura_store_analyzer_vercel` ou clique para selecionar a pasta
5. Na tela de configuração do projeto:
   - O nome do projeto será preenchido automaticamente, mas você pode alterá-lo
   - Framework Preset: Selecione "Other"
   - Root Directory: Mantenha como está (/)
   - Build Command: Deixe em branco
   - Output Directory: Deixe em branco
   - Install Command: Deixe em branco
6. Clique em "Deploy"
7. Aguarde a implantação ser concluída (geralmente leva menos de 1 minuto)
8. Quando terminar, você verá uma mensagem de sucesso e um link para seu site

### Opção B: Usando a CLI do Vercel (Para Usuários Avançados)

1. Instale a CLI do Vercel:
   ```bash
   npm install -g vercel
   ```

2. Navegue até a pasta do projeto:
   ```bash
   cd caminho/para/alura_store_analyzer_vercel
   ```

3. Faça login na sua conta Vercel:
   ```bash
   vercel login
   ```

4. Implante o projeto:
   ```bash
   vercel
   ```

5. Responda às perguntas:
   - Set up and deploy: Y
   - Which scope: Selecione sua conta pessoal
   - Link to existing project: N
   - Project name: Pressione Enter para usar o nome padrão ou digite um nome
   - In which directory is your code located: ./
   - Want to override settings: N

6. Aguarde a implantação ser concluída

## Passo 4: Testar a Aplicação

1. Após a implantação, você receberá um URL (algo como https://alura-store-analyzer-vercel.vercel.app)
2. Acesse o URL em seu navegador
3. Você deverá ver a interface do Alura Store Analyzer
4. Teste o upload de arquivos CSV e a análise de dados

## Passo 5: Configurar Domínio Personalizado (Opcional)

Se você deseja usar um domínio personalizado:

1. No dashboard do Vercel, acesse seu projeto
2. Clique na aba "Settings" e depois em "Domains"
3. Adicione seu domínio e siga as instruções para configurar os registros DNS

## Solução de Problemas

### Erro na Implantação

Se você encontrar erros durante a implantação:

1. Verifique os logs de implantação no dashboard do Vercel
2. Certifique-se de que a estrutura de pastas está correta
3. Verifique se o arquivo `vercel.json` está na raiz do projeto

### Erro ao Carregar a Aplicação

Se a aplicação não carregar corretamente:

1. Verifique se o URL está correto
2. Limpe o cache do navegador e tente novamente
3. Verifique os logs de função no dashboard do Vercel (Functions > Logs)

### Erro ao Processar Arquivos CSV

Se houver problemas ao processar arquivos CSV:

1. Verifique se os arquivos CSV estão no formato correto
2. Certifique-se de que os nomes das colunas correspondem aos esperados
3. Verifique se os arquivos não são muito grandes (limite de 4MB por arquivo)

## Recursos Adicionais

- [Documentação do Vercel](https://vercel.com/docs)
- [Guia de Serverless Functions do Vercel](https://vercel.com/docs/serverless-functions/introduction)
- [Fórum da Comunidade Vercel](https://github.com/vercel/vercel/discussions)

## Suporte

Se precisar de ajuda adicional, você pode:

1. Consultar o README.md principal para mais informações sobre o projeto
2. Verificar a documentação do Vercel para questões relacionadas à plataforma
3. Entrar em contato com o desenvolvedor para suporte específico da aplicação
