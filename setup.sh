#!/bin/bash

# Atualizar o sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python3 e pip
sudo apt install python3 python3-pip -y

# Instalar bibliotecas Python individualmente
pip3 install selenium
pip3 install webdriver_manager
pip3 install requests
pip3 install pyperclip
pip3 install geopy
pip3 install pydub
pip3 install beautifulsoup4
pip3 install dotenv
pip3 install flask  # Adicionando Flask

# Instalar Google Chrome e ChromeDriver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt update
sudo apt upgrade
sudo apt install ./google-chrome-stable_current_amd64.deb -y

# Instalar ffmpeg para dependências do pydub
sudo apt install ffmpeg -y

# Corrigir erros comuns atualizando bibliotecas
pip3 install --upgrade requests urllib3 chardet

# Instalar PM2 para gerenciamento de processos
sudo apt-get install nodejs npm -y
npm install pm2 -g

# Configurar PM2 para executar o script gerenciador.py
pm2 start ./gerenciador.py --name "gerenciador" --interpreter python3
