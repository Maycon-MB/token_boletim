import datetime
import sys
import jwt  
from db import Database

# Chave secreta para assinatura dos tokens JWT
SECRET_KEY = "teste"

# Obtendo os argumentos da linha de comando
args = sys.argv[1:]  # Ignora o primeiro argumento, que é o nome do script

# Verificando se foram fornecidos argumentos suficientes
if len(args) < 2:
    print("Os argumentos 'mat_prefix' e 'cot_prefix' não foram fornecidos. Gerando tokens para todos os contatos disponíveis...")
    mat_prefix = None
    cot_prefix = None
else:
    # Atribuindo os argumentos a 'mat_prefix' e 'cot_prefix'
    mat_prefix = args[0]
    cot_prefix = args[1]

# Função para gerar o token JWT
def gerar_token(avaliacao, mat):
    # Dados a serem incluídos no payload do token
    payload = {
        "avaliacao": avaliacao,
        "mat": mat,
    }
    # Gerar o token JWT assinado
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

if __name__ == "__main__":
    db = Database()
    try:
        # Obtendo os contatos com base nos dois primeiros dígitos de 'mat' e 'cot' da função pega_contatos_teste()
        contatos = db.pega_contatos_db(mat_prefix, cot_prefix)

        # Se não houver contatos disponíveis, exiba uma mensagem e saia
        if not contatos:
            print("Não foram encontrados contatos para gerar tokens. Todos já foram gerados.")
            sys.exit(1)

        hoje = datetime.date.today()
        dia_do_mes = hoje.day

        for contato in contatos:
            matricula = contato['mat']
            avaliacao = contato['avaliacao']

            # Verificar se o campo 'token' está vazio
            if not contato['token'] and contato['boletim'] is not None:
                # Gerar um novo token apenas se o campo estiver vazio
                token = gerar_token(avaliacao, matricula)
                # Atualizar o campo 'token' no dicionário de contato
                contato['token'] = token
                # Salvar o token no banco de dados
                db.inserir_token(matricula, token)
                print(f"Token gerado e salvo para {matricula}: {token}")
            else:
                # Se o campo 'token' já estiver preenchido, ignore
                print(f"Token já existente para {matricula}: {contato['token']}")

        # Commit de todas as alterações
        db.commit()
        print("Geração de tokens concluída.")
    finally:
        db.close()
