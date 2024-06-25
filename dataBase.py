import psycopg2
import logging

# Configurando o sistema de logging para o módulo db.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="BOLETOS",
            user="postgres",
            password="postgres",
            host="192.168.1.163"
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def inserir_token(self, mat, token):
        try:
            self.cursor.execute("UPDATE boletim_geral SET token = %s WHERE mat = %s AND token IS NULL AND boletim IS NOT NULL", (token, mat))
        except psycopg2.Error as e:
            logger.error("Erro ao inserir token no PostgreSQL: %s", e)

    def commit(self):
        self.conn.commit()

    def pega_contatos_db(self, mat_prefix=None, avaliacao_prefix=None):
        contatos = []
        try:
            if mat_prefix is not None and avaliacao_prefix is not None:
                self.cursor.execute("SELECT mat, nom, avaliacao, boletim, token, email, cpfa, cpf, cpf2, data_gerado FROM boletim_geral WHERE LEFT(mat, 2) = %s AND avaliacao = %s", (mat_prefix, avaliacao_prefix))
            else:
                self.cursor.execute("SELECT mat, nom, avaliacao, boletim, token, email, cpfa, cpf, cpf2, data_gerado FROM boletim_geral")

            rows = self.cursor.fetchall()
            for row in rows:
                contatos.append({
                    'mat': row[0],
                    'nome': row[1],
                    'avaliacao': row[2],
                    'boletim': row[3],
                    'token': row[4],
                    'email': row[5],
                    'cpfa': row[6],
                    'cpf': row[7],
                    'cpf2': row[8],
                    'data_gerado': row[9]
                })
        except psycopg2.Error as e:
            logger.error("Erro ao conectar ao PostgreSQL: %s", e)

        return contatos

