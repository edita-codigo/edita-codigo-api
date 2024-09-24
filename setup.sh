#!/bin/bash

# Receber o token e a porta via parâmetros da URL
TOKEN=${1:-xgLNUFtZsAbhZZaxkRh5ofM6Z0YIXwwv}
PORTA=${2:-5000}

# URL do repositório
REPO_URL="https://github.com/edita-codigo/edita-codigo-api.git"

# Clonar o repositório
echo "Clonando o repositório..."
git clone $REPO_URL api

# Criar o arquivo .env na pasta api
echo "Criando arquivo .env..."
cat <<EOT > api/.env
TOKEN=$TOKEN
PORTA=$PORTA
EOT

# Exibir mensagem de sucesso
echo "Arquivo .env criado com sucesso na pasta api. TOKEN: $TOKEN, PORTA: $PORTA."

# Executar o install.sh, se existir
if [ -f api/install.sh ]; then
    echo "Executando install.sh..."
    chmod +x api/install.sh
    cd api
    ./install.sh
else
    echo "install.sh não encontrado na pasta api."
fi
