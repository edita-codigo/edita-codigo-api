from flask import Flask, request, jsonify
import os
import subprocess
import shutil
from dotenv import load_dotenv
import threading
from queue import Queue

# Carregar as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Dicionário para armazenar filas por usuário
filas = {}

# Verificar se a chave é válida
def validar_chave(chave_recebida):
    chave_correta = os.getenv("TOKEN")
    return chave_recebida == chave_correta

# Função para processar a fila de cada usuário
def processar_fila(usuario):
    while True:
        data = filas[usuario].get()
        try:
            # Processar a requisição recebida na fila
            processar_requisicao(data)
        except Exception as e:
            print(f"Erro ao processar requisição para {usuario}: {e}")
        filas[usuario].task_done()

# Função para processar a requisição
def processar_requisicao(data):
    action = data.get('action')
    
    if action == 'iniciar_processo':
        caminho_script = data.get('caminho_script')
        usuario = data.get('usuario')
        iniciar_processo_pm2(caminho_script, usuario)
    elif action == 'stop_processo':
        usuario = data.get('usuario')
        stop_pm2(usuario)
    elif action == 'reset_processo':
        usuario = data.get('usuario')
        reset_pm2(usuario)
    elif action == 'deletar_processo':
        usuario = data.get('usuario')
        delete_pm2(usuario)
    else:
        print(f"Ação desconhecida: {action}")



# Função para substituir o TOKEN e PORTA no .env e reiniciar o PM2
def substituir_env(token_novo, porta_nova):
    caminho_env = '.env'
    
    # Ler o conteúdo do .env existente
    if os.path.exists(caminho_env):
        with open(caminho_env, 'r') as arquivo_env:
            linhas = arquivo_env.readlines()

        # Atualizar as variáveis TOKEN e PORTA
        with open(caminho_env, 'w') as arquivo_env:
            for linha in linhas:
                if linha.startswith('TOKEN='):
                    arquivo_env.write(f"TOKEN={token_novo}\n")
                elif linha.startswith('PORTA='):
                    arquivo_env.write(f"PORTA={porta_nova}\n")
                else:
                    arquivo_env.write(linha)
        
        print(f"Arquivo .env atualizado com TOKEN={token_novo} e PORTA={porta_nova}")
    else:
        return {"erro": ".env não encontrado"}

    # Reiniciar o processo pelo PM2
    resultado_reset = os.system("pm2 reset gerenciador")
    if resultado_reset == 0:
        print("PM2 resetado com sucesso.")
    else:
        print(f"Erro ao resetar PM2: {resultado_reset}")

    return {"sucesso": "Arquivo .env atualizado e PM2 resetado"}







 # Função para criar a conta
def criar_conta(usuario, diretorio_origem, diretorio_destino, servidor, token):
    # Criar os diretórios
    criar_diretorio(diretorio_destino)
    criar_diretorio(os.path.join(diretorio_destino, 'sessao'))
    criar_diretorio(os.path.join(diretorio_destino, 'download'))

    # Copiar os arquivos essenciais
    copiar_arquivo(os.path.join(diretorio_origem, 'bot.py'), os.path.join(diretorio_destino, 'bot.py'))
    copiar_arquivo(os.path.join(diretorio_origem, 'editacodigo.py'), os.path.join(diretorio_destino, 'editacodigo.py'))
    copiar_arquivo(os.path.join(diretorio_origem, 'api_manager.py'), os.path.join(diretorio_destino, 'api_manager.py'))
    copiar_arquivo(os.path.join(diretorio_origem, 'editafuncao.py'), os.path.join(diretorio_destino, 'editafuncao.py'))    
    copiar_arquivo(os.path.join(diretorio_origem, 'audio.wav'), os.path.join(diretorio_destino, 'audio.wav'))

    # Criar o arquivo .env com as informações necessárias
    caminho_env = os.path.join(diretorio_destino, '.env')
    with open(caminho_env, 'w') as arquivo_env:
        arquivo_env.write(f"USUARIO={usuario}\n")
        arquivo_env.write(f"DOWNLOAD_ARQUIVOS={os.path.join(diretorio_destino, 'download')}\n")
        arquivo_env.write(f"SESSAO_PASTA={os.path.join(diretorio_destino, 'sessao')}\n")
        arquivo_env.write(f"SERVIDOR={servidor}\n")
        arquivo_env.write(f"TOKEN={token}\n")
        arquivo_env.write(f"API=https://editacodigo.com.br/editacodigo/api/\n")

    print(f"Arquivo .env criado com sucesso para o usuário {usuario}")

    # Iniciar o processo no PM2 para o novo usuário
    caminho_script = os.path.join(diretorio_destino, 'bot.py')
    iniciar_processo_pm2(caminho_script, usuario)

# Deletar diretório
def deletar_diretorio(caminho):
    if os.path.exists(caminho):
        try:
            shutil.rmtree(caminho)
            print(f"Diretório '{caminho}' deletado com sucesso.")
        except OSError as erro:
            print(f"Erro ao deletar o diretório: {erro}")
    else:
        print(f"Diretório '{caminho}' não existe.")

def stop_pm2(usuario):
    # Comando PM2 para parar o processo pelo nome
    comando_pm2_stop = f"pm2 stop {usuario}"
    print("Comando PM2 Stop:", comando_pm2_stop)

    # Executando o comando PM2 para parar o processo
    resultado_stop = os.system(comando_pm2_stop)
    
    if resultado_stop == 0:
        print(f'Processo {usuario} parado com sucesso.')

        # Salvar o estado atual dos processos após parar
        comando_pm2_save = "pm2 save"
        print("Comando PM2 Save:", comando_pm2_save)
        resultado_save = os.system(comando_pm2_save)
        if resultado_save == 0:
            print('Estado atual dos processos salvo com sucesso após parar.')
        else:
            print(f'Falha ao salvar o estado dos processos após parar. Código de erro: {resultado_save}')
    else:
        print(f'Falha ao parar o processo {usuario}. Código de erro: {resultado_stop}')

# Iniciar processo no PM2
def iniciar_processo_pm2(caminho_script, nome_processo):
    print(f"Iniciando o processo PM2 para {nome_processo} com o script {caminho_script}")
    
    comando_pm2 = f"pm2 start {caminho_script} --name {nome_processo} --interpreter python3"
    resultado_start = os.system(comando_pm2)

    if resultado_start == 0:
        print(f'Processo {nome_processo} iniciado com sucesso.')
        os.system("pm2 save")
        os.system("pm2 startup")
    else:
        print(f'Falha ao iniciar o processo {nome_processo}. Código de erro: {resultado_start}')

# Reset processo no PM2
def reset_pm2(usuario):
    comando_pm2 = f"pm2 reset {usuario}"
    print(comando_pm2)

    # Executando o comando usando os.system
    resultado = os.system(comando_pm2)
    
    if resultado == 0:
        print(f'Processo {usuario} resetado com sucesso.')
    else:
        print(f'Falha ao resetar o processo {usuario}. Código de erro: {resultado}')

# Deletar processo no PM2
def delete_pm2(nome_processo):
    comando_pm2_delete = f"pm2 delete {nome_processo}"
    resultado_delete = os.system(comando_pm2_delete)

    if resultado_delete == 0:
        print(f'Processo {nome_processo} deletado com sucesso.')
        os.system("pm2 save")
    else:
        print(f'Falha ao deletar o processo {nome_processo}. Código de erro: {resultado_delete}')

# Criar diretórios
def criar_diretorio(caminho):
    try:
        os.makedirs(caminho, exist_ok=True)
        print(f"Diretório '{caminho}' criado com sucesso.")
    except OSError as erro:
        print(f"Erro ao criar o diretório: {erro}")

# Copiar arquivos entre diretórios
def copiar_arquivo(arquivo_origem, arquivo_destino):
    try:
        shutil.copy(arquivo_origem, arquivo_destino)
        print(f"Arquivo '{arquivo_origem}' copiado para '{arquivo_destino}'.")
    except IOError as erro:
        print(f"Erro ao copiar arquivo: {erro}")

# Rota para iniciar processo com fila
@app.route('/iniciar_processo', methods=['POST'])
def iniciar_processo():
    dados = request.json
    print(dados)

    chave_recebida = dados.get('chave')
    if not validar_chave(chave_recebida):
        return jsonify({"erro": "Chave inválida"}), 403

    caminho_script = dados.get('caminho_script')
    nome_processo = dados.get('usuario')  # Nome do processo será o CPF, por exemplo
    if not caminho_script or not nome_processo:
        return jsonify({"erro": "Parâmetros faltando"}), 400

    # Inicializar fila para o usuário se não existir
    if nome_processo not in filas:
        filas[nome_processo] = Queue()
        threading.Thread(target=processar_fila, args=(nome_processo,), daemon=True).start()

    # Colocar a requisição na fila do usuário
    filas[nome_processo].put(dados)

    return jsonify({"sucesso": f"Processo {nome_processo} adicionado à fila."})

# Rota para parar processo com fila
@app.route('/stop_processo', methods=['POST'])
def stop_processo():
    dados = request.json
    print(dados)

    chave_recebida = dados.get('chave')
    if not validar_chave(chave_recebida):
        return jsonify({"erro": "Chave inválida"}), 403

    nome_processo = dados.get('usuario')

    if not nome_processo:
        return jsonify({"erro": "Parâmetros faltando"}), 400

    # Inicializar fila para o usuário se não existir
    if nome_processo not in filas:
        filas[nome_processo] = Queue()
        threading.Thread(target=processar_fila, args=(nome_processo,), daemon=True).start()

    # Colocar a requisição na fila do usuário
    filas[nome_processo].put(dados)

    return jsonify({"sucesso": f"Processo {nome_processo} adicionado à fila."})



@app.route('/substituir_env', methods=['POST'])
def substituir_env_route():
    dados = request.json
    #token_novo = dados.get('token_novo')
    chave_recebida = dados.get('chave')
    if not validar_chave(chave_recebida):
        return jsonify({"erro": "Chave inválida"}), 403


    token_novo = dados.get('token')
    porta_nova = dados.get('porta')

    if not token_novo or not porta_nova:
        return jsonify({"erro": "Parâmetros faltando: token ou porta"}), 400

    resultado = substituir_env(token_novo, porta_nova)
    return jsonify(resultado)







# Rota para resetar processo com fila
@app.route('/reset_processo', methods=['POST'])
def reset_processo():
    dados = request.json
    print(dados)

    chave_recebida = dados.get('chave')
    if not validar_chave(chave_recebida):
        return jsonify({"erro": "Chave inválida"}), 403

    nome_processo = dados.get('usuario')

    if not nome_processo:
        return jsonify({"erro": "Parâmetros faltando"}), 400

    # Inicializar fila para o usuário se não existir
    if nome_processo not in filas:
        filas[nome_processo] = Queue()
        threading.Thread(target=processar_fila, args=(nome_processo,), daemon=True).start()

    # Colocar a requisição na fila do usuário
    filas[nome_processo].put(dados)

    return jsonify({"sucesso": f"Processo {nome_processo} adicionado à fila."})

# Rota para deletar processo com fila
@app.route('/deletar_processo', methods=['POST'])
def deletar_processo():
    dados = request.json
    chave_recebida = dados.get('chave')
    if not validar_chave(chave_recebida):
        return jsonify({"erro": "Chave inválida"}), 403

    nome_processo = dados.get('usuario')

    if not nome_processo:
        return jsonify({"erro": "Parâmetros faltando"}), 400

    # Inicializar fila para o usuário se não existir
    if nome_processo not in filas:
        filas[nome_processo] = Queue()
        threading.Thread(target=processar_fila, args=(nome_processo,), daemon=True).start()

    # Colocar a requisição na fila do usuário
    filas[nome_processo].put(dados)

    return jsonify({"sucesso": f"Processo {nome_processo} adicionado à fila."})

if __name__ == '__main__':
    # Carregar a porta do .env
    porta = int(os.getenv("PORTA", 5000))  # Se não encontrar no .env, usará a porta 5000 por padrão
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=porta)
