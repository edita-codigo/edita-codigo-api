import requests
import base64
import importlib.util
import io
import sys

def safe_base64_decode(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return base64.b64decode(data)

def vect(var):
    x = ((8 * 3 - 4 ** 2 + (10 // 5) * 3) // 2) + (45 % 7) - ((3 * 2) // 6) 
    return var[x:]

def load_editacodigo(api_url, token):
    data = {'token': token}
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    response = requests.post(api_url, data=data, headers=headers)
    response_data = response.json()

    if response_data['status'] == 'success':
        base64_url = response_data.get('url_base64')
        base64_username = response_data.get('username_base64')
        base64_password = response_data.get('password_base64')

        if base64_url:
            file_url = safe_base64_decode(vect(base64_url)).decode('utf-8')
            username = base64.b64decode(vect(base64_username)).decode('utf-8')
            password = base64.b64decode(vect(base64_password)).decode('utf-8')

            response_file = requests.get(file_url, auth=(username, password))
            if response_file.status_code == 200:
                code_content = response_file.content
                code_module = io.StringIO(code_content.decode('utf-8'))
                spec = importlib.util.spec_from_loader("editacodigo", loader=None)
                editacodigo = importlib.util.module_from_spec(spec)
                exec(code_content, editacodigo.__dict__)
                sys.modules["editacodigo"] = editacodigo
                return editacodigo
            else:
                print(f"Falha ao acessar o arquivo: {response_file.status_code}")
        else:
            print("URL base64 não fornecida na resposta da API.")
    else:
        print("Erro ao obter a URL:", response_data['message'])
    return None
