import time
import requests
import json
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
import threading
from editafuncao import *
from queue import Queue
from functools import wraps
import requests
import base64
import importlib.util
import io
import sys
from api_manager import load_editacodigo
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys





app = Flask(__name__)

# Carrega as variáveis de ambiente do arquivo .env no diretório atual
load_dotenv()

# Acessando as variáveis usando os.environ
download_arquivos = os.environ.get('DOWNLOAD_ARQUIVOS')
sessao_pasta = os.environ.get('SESSAO_PASTA')
site = os.environ.get('SITE')
servidor = os.environ.get('WEBHOOK')
usuario = os.environ.get('USUARIO')

porta = os.environ.get('PORTA')
api = os.environ.get('API')
token = os.environ.get('TOKEN')

agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

# Imprimindo as variáveis
print("DOWNLOAD_ARQUIVOS:", download_arquivos)
print("SESSAO_PASTA:", sessao_pasta)
print("SITE:", site)
print("WEBHOOK:", servidor)
print("USUARIO:", usuario)
print("PORTA:", porta)
print("API:", api)
print("TOKEN:", token)

api_url = api
token = token


editacodigo = load_editacodigo(api_url, token)

classes = editacodigo.obter_classes_whatsapp(token)

#ESSE ABE VIA TRMINAL PRA RODAR EM VPS
driver = editacodigo.carregar_chrome_terminal_audio(download_arquivos,sessao_pasta,site)

#ESSE ABRE EM NAVEGADOR VISIVEL
#driver = editacodigo.carregar_chrome_audio(download_arquivos,sessao_pasta,site)

filas = {}




def verificar_mensagens():
    enquetes_processadas = set()  # Conjunto para armazenar enquetes já processadas
    
    while True:
        try:
            # Primeira tentativa: Verificar novas mensagens
            print('verficando mensagens')
            editacodigo.MensagemRecebida(driver,usuario, servidor, download_arquivos, **classes)
        except Exception as e:
            print(f"Erro ao verificar mensagens: {e}")
        try:
            # Segunda tentativa: Verificar novas enquetes, passando `enquetes_processadas` como argumento
            telefone_enquete, mensagem_enquete = editacodigo.PegaEnquete(driver,enquetes_processadas,servidor,**classes)

            # Verificar se a enquete já foi processada com base na mensagem completa
            if telefone_enquete and mensagem_enquete and (telefone_enquete, mensagem_enquete) not in enquetes_processadas:
                print(f"Nova enquete detectada para o número {telefone_enquete}.")
                enquetes_processadas.add((telefone_enquete, mensagem_enquete))  # Adiciona ao conjunto de enquetes processadas
                # Enviar o request ou qualquer outra ação necessária aqui

            else:
                print(f"Enquete já processada ou não detectada para o número {telefone_enquete}.")

        except Exception as e:
            print(f"Erro ao verificar enquetes: {e}")

        time.sleep(1)  # Ajuste o tempo de espera conforme necessário
        #editacodigo.fecha_conversa(driver)


################################################################################################################
##############################################################s##################################################

def processar_fila(usuario):
    while True:
        data = filas[usuario].get()
        try:
            processar_requisicao(data)
        except Exception as e:
            print(f"Erro ao processar requisição para {usuario}: {e}")
        filas[usuario].task_done()

################################################################################################################
################################################################################################################

def usuario_autorizado(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.json
        usuario_recebido = data.get('usuario')
        token_recebido = data.get('token')
        
        # Comparar usuario e token com os valores no arquivo .env
        if not usuario_recebido or usuario_recebido != usuario:
            return jsonify({'status': 'unauthorized', 'message': 'Usuário não autorizado ou não fornecido'}), 403
        
        if not token_recebido or token_recebido != token:
            return jsonify({'status': 'unauthorized', 'message': 'Token não autorizado ou não fornecido'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


################################################################################################################
################################################################################################################
@app.route('/webhook', methods=['POST'])
@usuario_autorizado
def webhook():
    data = request.json
    usuario_recebido = data['usuario']
    
    # Inicializar fila para o usuário se não existir
    if usuario_recebido not in filas:
        filas[usuario_recebido] = Queue()
        threading.Thread(target=processar_fila, args=(usuario_recebido,), daemon=True).start()
    
    # Colocar a requisição na fila do usuário
    filas[usuario_recebido].put(data)
    return jsonify({'status': 'accepted'})




################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################



def processar_requisicao(data):
    if 'action' in data:
        if data['action'] == 'GerarQrcode':
            try:
                mensagem = data['message']

                qr_code_texto = editacodigo.GerarQrcode(driver, usuario, servidor, **classes)
                print(f"QR Code gerado: {qr_code_texto}")
            except Exception as e:
                print(f"Erro ao gerar QR Code: {e}")
        elif data['action'] == 'EnviarMsg':
            try:
                mensagem = data['message']
                telefone = mensagem['telefone']
                msg = mensagem['msg']
                id_msg = mensagem['id_msg']

                # Adicione o processamento da mensagem aqui
                print(f"Nova mensagem de {telefone}: {msg}")
                editacodigo.EnviarMsg(driver, telefone,msg,servidor,id_msg,usuario,**classes)
                time.sleep(1)
                editacodigo.fecha_conversa(driver)
            except Exception as e:
                print(f"Erro ao processar nova mensagem: {e}")

        elif data['action'] == 'EnviarMsgMidia':
            try:
                mensagem = data['message']
                telefone = mensagem['telefone']
                msg = mensagem['msg']
                url = mensagem['url']
                tipo = mensagem['tipo']
                id_msg = mensagem['id_msg']
               
                # Adicione o processamento da mensagem aqui
                print(f"Nova mensagem de {telefone}: {msg}")
                editacodigo.EnviarMsgMidia(driver, url, tipo, telefone,servidor,msg,id_msg,usuario,**classes)
                time.sleep(0.5)
                editacodigo.fecha_conversa(driver)
            except Exception as e:
                print(f"Erro ao processar nova mensagem: {e}")   


        elif data['action'] == 'ContatosNaoSalvos':
            try:
               
                
                editacodigo.ContatosNaoSalvos(driver,servidor, usuario,**classes)
                time.sleep(0.3)
                editacodigo.fecha_conversa(driver)
            except Exception as e:
                print(f"Erro ao processar nova mensagem: {e}")   

        elif data['action'] == 'ExtrairTelefonesGrupos':
            try:
                mensagem = data['message']
                nome_grupo = mensagem['nome_grupo']

                # Adicione o processamento da mensagem aqui
                
                editacodigo.ExtrairTelefonesGrupos(driver,nome_grupo,servidor,usuario,**classes)
                editacodigo.fecha_conversa(driver)
                time.sleep(0.3)
                editacodigo.fecha_conversa(driver)
                time.sleep(0.3)
                editacodigo.ClicarX(driver,**classes)
            except Exception as e:
                print(f"Erro ao processar nova mensagem: {e}")   

        elif data['action'] == 'EscreverEnquete':
            try:
                mensagem = data['message']
                telefone = mensagem['telefone']
                enquete = mensagem['enquete']
                id_comando = 1
                # Adicione o processamento da mensagem aqui
                
                editacodigo.EscreverEnquete(driver,telefone,enquete,**classes)
                time.sleep(1)
                editacodigo.fecha_conversa(driver)
             
            except Exception as e:
                print(f"Erro ao processar nova mensagem: {e}")                    
        
        elif data['action'] == 'EscreverEnqueteEmoticon':
            try:
                mensagem = data['message']
                telefone = mensagem['telefone']
                enquete = mensagem['enquete']
                # Adicione o processamento da mensagem aqui
                
                editacodigo.EscreverEnqueteEmoticon(driver,telefone,enquete,**classes)
                time.sleep(1)
                editacodigo.fecha_conversa(driver)
             
            except Exception as e:
                print(f"Erro ao processar nova mensagem: {e}")                    

        elif data['action'] == 'GravarAudio':
            try:
                mensagem = data['message']
                telefone = mensagem['telefone']
                url = mensagem['url']
                # Adicione o processamento da mensagem aqui
                
                editacodigo.GravarAudio(driver,telefone,url,**classes)
                editacodigo.fecha_conversa(driver)

            except Exception as e:
                print(f"Erro ao processar nova mensagem: {e}")             
##########################################################################################
##########################################################################################
##########################################################################################                             
        else:
            print(f"Ação desconhecida: {data['action']}")
    else:
        print("Nenhuma ação fornecida")

if __name__ == '__main__':
    # Iniciar a thread para verificar mensagens
    threading.Thread(target=verificar_mensagens, daemon=True).start()
    # Iniciar o servidor Flask
    #app.run(port=porta)
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=porta)

