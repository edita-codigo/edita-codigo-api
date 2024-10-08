# Edita-Codigo API

A **Edita-Codigo API** é uma API de automação para WhatsApp que utiliza **Selenium** para interagir com a interface web do WhatsApp e **Flask** para comunicação via endpoints HTTP. Com esta API, você pode enviar mensagens, mídias, gerenciar enquetes, extrair contatos de grupos, entre outras funcionalidades.

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
  - [Obtenção do Token](#obtenção-do-token)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Gerenciamento de Processos com PM2](#gerenciamento-de-processos-com-pm2)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Suporte](#suporte)
- [Licença](#licença)
- [Aviso Legal](#aviso-legal)

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
   git clone https://github.com/edita-codigo/edita-codigo-api.git
   cd edita-codigo-api
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

### Obtenção do Token

Para utilizar a API, é necessário obter um **Token de Autenticação**. Você pode adquirir um token **gratuitamente** no site da Edita Código. Siga os passos abaixo para obter o seu token:

1. **Acesse o Site da Edita Código:**

   Visite o seguinte link:

   [Obtenha seu Token Aqui](https://editacodigo.com.br/editacodigo/api_detalhes.php)

2. **Crie uma Conta ou Faça Login:**

   - **Novo Usuário:**
     - Clique em **"Cadastrar"** ou **"Registrar"**.
     - Preencha os dados solicitados (nome, e-mail, senha, etc.).
     - Confirme o cadastro através do e-mail de verificação, se aplicável.

   - **Usuário Existente:**
     - Clique em **"Login"** ou **"Entrar"**.
     - Insira suas credenciais (e-mail e senha) para acessar sua conta.

3. **Navegue até a Seção de APIs:**

   - Após o login, procure pelo menu ou seção intitulada **"APIs"**, **"Serviços"** ou similar.
   - Clique em **"Detalhes da API"** ou **"Obter Token"**.

4. **Obtenha o Seu Token:**

   - Siga as instruções para gerar ou visualizar o seu token de autenticação.
   - O token geralmente é uma sequência de caracteres alfanuméricos única.
   - **Copie o Token** e guarde-o em um lugar seguro.



Aqui está o trecho que você pode adicionar ao seu `README.md`, oferecendo a opção de alterar o código no arquivo `bot.py` para rodar a API via terminal ou abrir um navegador visível:

---

### Alteração de Modo de Execução do Navegador

Você pode configurar a API para rodar o navegador Chrome de duas maneiras diferentes no arquivo `bot.py`:

1. **Execução via Terminal (Headless Mode)**: O navegador rodará em modo invisível, ideal para VPS.
2. **Execução com Navegador Visível**: O navegador será aberto visivelmente para monitoramento manual.

#### Como Alterar:

- **Rodar via Terminal (Headless)**:

  Para rodar o Chrome em modo terminal (sem abrir o navegador visível), utilize o seguinte código no arquivo `bot.py`:

  ```python
  driver = editacodigo.carregar_chrome_terminal_audio(download_arquivos, sessao_pasta, site)
  ```

- **Rodar com Navegador Visível**:

  Caso queira que o navegador Chrome seja aberto visivelmente, com interface gráfica, use a linha abaixo (remova o comentário):

  ```python
  #driver = editacodigo.carregar_chrome_audio(download_arquivos, sessao_pasta, site)
  ```

**Por padrão**, o navegador está configurado para rodar via terminal. Se você quiser abrir o navegador visível, remova o `#` no início da linha correspondente e comente a linha que roda no terminal.

---

Esse trecho pode ser facilmente editado por você no `README.md`, oferecendo flexibilidade para quem quiser modificar o modo de execução do navegador no código.
**Importante:**

- **Segurança do Token:**
  - O token é uma credencial sensível que permite o acesso à API.
  - **Não compartilhe** o seu token com terceiros.
  - Evite expor o token em repositórios públicos ou em código-fonte compartilhado.

- **Limitações e Restrições:**
  - Verifique se há alguma limitação de uso ou restrições associadas ao token gratuito.
  - Algumas APIs podem ter limites de requisições por minuto ou por dia.

- **Suporte e Ajuda:**
  - Se encontrar dificuldades para obter o token, entre em contato com o suporte da Edita Código através do site ou dos canais de contato disponíveis.

### Configuração do Arquivo `.env`

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
TOKEN=SEU_TOKEN_AQUI
```

**Descrição das Variáveis:**

- `USUARIO`: Nome de usuário para autenticação.
- `DOWNLOAD_ARQUIVOS`: Caminho para o diretório onde os arquivos baixados serão armazenados.
- `SESSAO_PASTA`: Caminho para o diretório de sessão do Selenium.
- `WEBHOOK`: URL do webhook para integração.
- `SITE`: URL do WhatsApp Web.
- `PORTA`: Porta na qual a API Flask será executada.
- `API`: URL da API utilizada para gerenciar ações.
- `TOKEN`: **Seu Token de Autenticação** obtido no site da Edita Código.

### Configurar PM2

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
- `AVISO_LEGAL.md`: Arquivo contendo o aviso legal separado.
- `LICENSE`: Arquivo de licença MIT.
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
           "token": "SEU_TOKEN_AQUI",
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
           "chave": "SEU_TOKEN_AQUI",
           "caminho_script": "/caminho/para/bot.py",
           "usuario": "usuario_exemplo"
         }'
```

## Suporte

Para suporte, você pode:

- **Entrar no Grupo do WhatsApp:**

  [Grupo de Suporte no WhatsApp](https://chat.whatsapp.com/Ezuudcc4qPg1cfWuBxNFiM)

- **Contato Direto com o Desenvolvedor:**

  [WhatsApp do Desenvolvedor](https://wa.me/EDITACODIGO)

## Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).

---

## Aviso Legal

Para mais informações sobre o uso responsável e as isenções de responsabilidade, consulte o [Aviso Legal](AVISO_LEGAL.md).

---

**Nota:** Certifique-se de manter o arquivo `.env` seguro e nunca compartilhá-lo publicamente, pois ele contém informações sensíveis como tokens e configurações de acesso.

---



**Estrutura do Repositório:**

```
edita-codigo-api/
├── AVISO_LEGAL.md
├── LICENSE
├── README.md
├── setup.sh
├── gerenciador.py
├── bot.py
├── .env
├── editacodigo.py
├── api_manager.py
├── editafuncao.py

```

**Links Importantes:**

- [Repositório no GitHub](https://github.com/edita-codigo/edita-codigo-api.git)
- [Licença MIT](https://opensource.org/licenses/MIT)
- [Grupo de Suporte no WhatsApp](https://chat.whatsapp.com/Ezuudcc4qPg1cfWuBxNFiM)
- [WhatsApp do Desenvolvedor](https://wa.me/EDITACODIGO)
- [Obtenha seu Token Aqui](https://editacodigo.com.br/editacodigo/api_detalhes.php)

