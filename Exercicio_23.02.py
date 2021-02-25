
# Modelar um sistema de gerenciamento de banco de dados de alunos para Universidades Com as seguintes considerações:

# Você deverá cadastrar as seguintes informações de cada profissional da Universidade (Alunos e Professores):
# Primeiro nome; Sobrenome; Data de nascimento ; email do aluno
# Cada aluno poderá se matricular em um determinado curso dado por um determinado professor
# Cada aluno poderá realizar o mesmo curso até 3 vezes, sendo aprovado quando obter média >= 70.0
# Definir as tabelas (entities) com seu respectivos atributos - definir os "constraints" e as chaves primárias e/ou estrangeiras

import os, sys, sqlite3
os.chdir(sys.path[0]) #seleciono o caminho atual como padrão
address = os.path.join('files', 'universidade.db')

db = sqlite3.connect(address) #Cria o bd se não existir
cursor = db.cursor() #Cria um cursor para fazer as operações com o banco de dados
cursor.execute("PRAGMA foreign_keys = ON").fetchall()

#Person Table
person_db = """CREATE TABLE IF NOT EXISTS person (
id INT NOT NULL PRIMARY KEY,
first_name TEXT,
last_name TEXT,
email TEXT,
birth DATE);
"""

#Teacher Table
teacher_db = """CREATE TABLE IF NOT EXISTS teacher (
id INT NOT NULL PRIMARY KEY,
person_id INT NOT NULL REFERENCES person(id),
registration int);
"""
#Teacher Table
cursor.execute(person_db) #Executa a tabela pessoa
cursor.execute(teacher_db) #Executa a tabela professores

print(cursor.execute("PRAGMA table_info(person)").fetchall())
#print(cursor.fetchall())
"""
class insert:
    def __init__(self, first_name, last_name, birth, email):
        self.first_name = 

p1 = insert()

if __name__=="__main__":
    nome = input("Por favor, insira o nome da pessoa\n")
"""
db.close() #Fecha a conexão com o bd	