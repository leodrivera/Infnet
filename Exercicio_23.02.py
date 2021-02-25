
# Modelar um sistema de gerenciamento de banco de dados de alunos para Universidades Com as seguintes considerações:

# Você deverá cadastrar as seguintes informações de cada profissional da Universidade (Alunos e Professores):
# Primeiro nome; Sobrenome; Data de nascimento ; email do aluno
# Cada aluno poderá se matricular em um determinado curso dado por um determinado professor
# Cada aluno poderá realizar o mesmo curso até 3 vezes, sendo aprovado quando obter média >= 70.0
# Definir as tabelas (entities) com seu respectivos atributos - definir os "constraints" e as chaves primárias e/ou estrangeiras

import os, sys, re, sqlite3

class Pessoa:
    def __init__(self):
        self.first_name = input("Por favor, insira o *primeiro nome* da pessoa:\n")
        self.last_name = input("Por favor, insira o *último nome* da pessoa:\n")
        self.birth = input("Por favor, insira a *data de nascimento* da pessoa:\n")
        self.email = input("Por favor, insira o *e-mail* da pessoa:\n")

        cursor.execute("INSERT INTO person (first_name,last_name,email,birth) VALUES (?,?,?,?)", (self.first_name, self.last_name, self.birth, self.email,))
        
if __name__=="__main__":

    os.chdir(sys.path[0]) #seleciono o caminho atual como padrão
    address = os.path.join('files', 'universidade.db')

    db = sqlite3.connect(address) #Cria o bd se não existir
    cursor = db.cursor() #Cria um cursor para fazer as operações com o banco de dados
    cursor.execute("PRAGMA foreign_keys = ON").fetchall()

    #Person Table
    person_db = """CREATE TABLE IF NOT EXISTS person (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    birth DATE);
    """

    #Teacher Table
    teacher_db = """CREATE TABLE IF NOT EXISTS teacher (
    id INTEGER NOT NULL PRIMARY KEY,
    person_id INTEGER NOT NULL REFERENCES person(id),
    registration INTEGER);
    """
    #Teacher Table
    cursor.execute(person_db) #Executa a tabela pessoa
    cursor.execute(teacher_db) #Executa a tabela professores

    while 1:
        print("***Sistema de Gerenciamento dos Dados da Universidade.***")
        print("Escolha uma das opções abaixo ou digite qualquer outro caracter para sair:.")        
        print("'1' - Realizar um cadastro.")
        print("'2' - Realizar uma consulta.")
        resp = input("")
        if resp == '1':
            print(f"Resposta {resp}")
            while 1:
                print("O que deseja cadastrar? (Digite qualquer outro caracter para sair):")
                print("'1' - Aluno.")
                print("'2' - Professor.")
                print("'3' - Curso.")
                print("'4' - Aluno em curso ")
                print("'5' - Nota.")
                resp = input("")
                if resp == '1':
                    print(f"Resposta {resp}")
                    pessoa = Pessoa()
                    cursor_head = db.execute('select * from person') #cursos para pegar o cabecalho
                    print([description[0] for description in cursor_head.description]) #imprimo o cabecalho
                    print(cursor.execute('SELECT * FROM person').fetchall())
                    db.commit() #executa as mudanças no bd
                elif resp == '2':
                    print(f"Resposta {resp}")
                elif resp == '3':
                    print(f"Resposta {resp}")
                elif resp == '4':
                    print(f"Resposta {resp}")
                elif resp == '5':
                    print(f"Resposta {resp}")
                else:
                    print("Saindo do módulo cadastro.")
                    break
        elif resp == '2':
            print("Resposta 2")
            while 1:
                print("O que deseja consultar?")
                print("'1' - Alunos cadastradas.")
                print("'2' - Professores cadastradas.")
                print("'3' - Cursos existentes.")
                print("'4' - Média dos alunos.")
                resp = input("")
                if resp == '1':
                    print(f"Resposta {resp}")
                elif resp == '2':
                    print(f"Resposta {resp}")
                elif resp == '3':
                    print(f"Resposta {resp}")
                elif resp == '4':
                    print(f"Resposta {resp}")
                else:
                    print("Saindo do módulo consulta.")
                    break
        else:
            print("Saindo do programa.")
            break
    db.close() #Fecha a conexão com o bd
            	