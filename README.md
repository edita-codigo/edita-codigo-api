# API de Automação de WhatsApp com Selenium e Flask

Esta API permite a automação de ações no WhatsApp utilizando Selenium para interagir com a interface web do WhatsApp e Flask para comunicação via endpoints HTTP. Com esta API, você pode enviar mensagens, mídias, gerenciar enquetes, extrair contatos de grupos, entre outras funcionalidades.

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Gerenciamento de Processos com PM2](#gerenciamento-de-processos-com-pm2)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados no seu sistema:

- **Sistema Operacional**: Ubuntu ou outra distribuição Linux baseada em Debian
- **Python 3.6+**
- **Node.js e npm**
- **Google Chrome** (a versão será instalada automaticamente pelo script)
- **Git** (opcional, para clonar o repositório)

## Instalação

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie o Script de Instalação**

   Certifique-se de ter o script `setup.sh` fornecido. Se ainda não o criou, crie um arquivo chamado `setup.sh` e adicione o conteúdo abaixo:

   ```bash
   #!/bin/bash

   # Atualizar o sistema
   sudo apt update && sudo apt upgrade -y

   # Instalar Python3 e pip
   sudo apt install python3 python3-pip -y

   # Instalar bibliotecas Python individualmente
   pip3 install selenium
   pip3 install webdriver_manager
   pip3 install requests
   pip3 install pydub
   pip3 install beautifulsoup4
   pip3 install python-dotenv
   pip3 install flask  # Adicionando Flask

   # Instalar Google Chrome e ChromeDriver
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo apt update
   sudo apt upgrade
   sudo apt install ./google-chrome-stable_current_amd64.deb -y

   # Corrigir erros comuns atualizando bibliotecas
   pip3 install --upgrade requests urllib3 chardet

   # Instalar PM2 para gerenciamento de processos
   sudo apt-get install nodejs npm -y
   npm install pm2 -g

   # Configurar PM2 para executar o script gerenciador.py
   pm2 start ./gerenciador.py --name "gerenciador" --interpreter python3
   ```

3. **Torne o Script Executável e Execute-o**

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

## Configuração

1. **Arquivo `.env`**

   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

   ```env
   # Informações do usuário
   USUARIO=seu_usuario_aqui

   # Diretórios
   DOWNLOAD_ARQUIVOS=/caminho/para/download
   SESSAO_PASTA=/caminho/para/sessao

   # Configurações do servidor
   WEBHOOK=http://seu_site
   SITE=https://web.whatsapp.com
   PORTA=5000  # Altere conforme necessário
   API=https://editacodigo.com.br/api/
   TOKEN=EDITACODIGO
   ```

   **Descrição das Variáveis:**

   - `USUARIO`: Nome de usuário para autenticação.
   - `DOWNLOAD_ARQUIVOS`: Caminho para o diretório onde os arquivos baixados serão armazenados.
   - `SESSAO_PASTA`: Caminho para o diretório de sessão do Selenium.
   - `WEBHOOK`: URL do webhook para integração.
   - `SITE`: URL do WhatsApp Web.
   - `PORTA`: Porta na qual a API Flask será executada.
   - `API`: URL da API utilizada para gerenciar ações.
   - `TOKEN`: Token de autenticação para a API.

2. **Configurar PM2**

   O PM2 já está configurado para iniciar o `gerenciador.py` automaticamente durante a execução do `setup.sh`. Para garantir que o processo seja mantido em execução, você pode salvar a configuração do PM2:

   ```bash
   pm2 save
   pm2 startup
   ```

## Uso

1. **Iniciar a API**

   Se o script de setup foi executado corretamente, o PM2 já estará gerenciando o processo `gerenciador`. Caso precise iniciar manualmente:

   ```bash
   pm2 start gerenciador.py --name "gerenciador" --interpreter python3
   ```

2. **Acessar a API**

   A API estará disponível na porta definida no arquivo `.env` (por padrão, `http://localhost:5000`). Você pode interagir com a API enviando requisições HTTP para os endpoints disponíveis.

## Estrutura do Projeto

- `setup.sh`: Script de instalação e configuração do ambiente.
- `gerenciador.py`: Script principal que gerencia o bot, recebe comandos via CURL e interage com o PM2.
- `bot.py`: Arquivo principal que contém a lógica do bot utilizando Selenium e Flask.
- `.env`: Arquivo de configuração de variáveis de ambiente.
- Outros arquivos auxiliares: `editacodigo.py`, `api_manager.py`, `editafuncao.py`, etc.

## Gerenciamento de Processos com PM2

O PM2 é utilizado para gerenciar os processos da API, garantindo que os scripts estejam sempre em execução e reiniciando-os em caso de falhas.

**Comandos Úteis do PM2:**

- **Listar Processos:**

  ```bash
  pm2 list
  ```

- **Parar um Processo:**

  ```bash
  pm2 stop gerenciador
  ```

- **Reiniciar um Processo:**

  ```bash
  pm2 restart gerenciador
  ```

- **Deletar um Processo:**

  ```bash
  pm2 delete gerenciador
  ```

- **Salvar a Configuração Atual:**

  ```bash
  pm2 save
  ```

- **Configurar PM2 para Iniciar na Inicialização do Sistema:**

  ```bash
  pm2 startup
  ```

## Endpoints Disponíveis

### 1. **Webhook**

- **URL:** `/webhook`
- **Método:** `POST`
- **Descrição:** Recebe comandos para a API processar ações no WhatsApp.
- **Autenticação:** Token e usuário via corpo da requisição.

**Exemplo de Requisição:**

```bash
curl -X POST http://localhost:5000/webhook \
     -H "Content-Type: application/json" \
     -d '{
           "usuario": "seu_usuario_aqui",
           "token": "EDITACODIGO",
           "action": "EnviarMsg",
           "message": {
               "telefone": "5511999999999",
               "msg": "Olá, esta é uma mensagem automatizada!",
               "id_msg": "12345"
           }
         }'
```

### 2. **Gerenciar Processos**

- **Iniciar Processo:**
  - **URL:** `/iniciar_processo`
  - **Método:** `POST`
  - **Descrição:** Inicia um novo processo gerenciado pelo PM2.
  - **Parâmetros:**
    - `chave`: Chave de autenticação.
    - `caminho_script`: Caminho para o script a ser executado.
    - `usuario`: Nome do usuário/projeto.

- **Parar Processo:**
  - **URL:** `/stop_processo`
  - **Método:** `POST`
  - **Descrição:** Para um processo específico.
  - **Parâmetros:**
    - `chave`: Chave de autenticação.
    - `usuario`: Nome do usuário/projeto.

- **Resetar Processo:**
  - **URL:** `/reset_processo`
  - **Método:** `POST`
  - **Descrição:** Reseta um processo específico.
  - **Parâmetros:**
    - `chave`: Chave de autenticação.
    - `usuario`: Nome do usuário/projeto.

- **Deletar Processo:**
  - **URL:** `/deletar_processo`
  - **Método:** `POST`
  - **Descrição:** Deleta um processo específico.
  - **Parâmetros:**
    - `chave`: Chave de autenticação.
    - `usuario`: Nome do usuário/projeto.

- **Substituir Variáveis de Ambiente:**
  - **URL:** `/substituir_env`
  - **Método:** `POST`
  - **Descrição:** Substitui o `TOKEN` e a `PORTA` no arquivo `.env` e reinicia o PM2.
  - **Parâmetros:**
    - `chave`: Chave de autenticação.
    - `token`: Novo token.
    - `porta`: Nova porta.

**Exemplo de Requisição para Iniciar Processo:**

```bash
curl -X POST http://localhost:5000/iniciar_processo \
     -H "Content-Type: application/json" \
     -d '{
           "chave": "EDITACODIGO",
           "caminho_script": "/caminho/para/bot.py",
           "usuario": "usuario_exemplo"
         }'
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

1. **Fork o Repositório**
2. **Crie sua Feature Branch**

   ```bash
   git checkout -b feature/nova-feature
   ```

3. **Commit suas Alterações**

   ```bash
   git commit -m "Adiciona nova feature"
   ```

4. **Push para a Branch**

   ```bash
   git push origin feature/nova-feature
   ```

5. **Abra um Pull Request**

## Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).

---

**Nota:** Certifique-se de manter o arquivo `.env` seguro e nunca compartilhá-lo publicamente, pois ele contém informações sensíveis como tokens e configurações de acesso.