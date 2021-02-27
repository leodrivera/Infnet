
# Modelar um sistema de gerenciamento de banco de dados de alunos para Universidades Com as seguintes considerações:

# Você deverá cadastrar as seguintes informações de cada profissional da Universidade (Alunos e Professores):
# Primeiro nome; Sobrenome; Data de nascimento ; email do aluno
# Cada aluno poderá se matricular em um determinado curso dado por um determinado professor
# Cada aluno poderá realizar o mesmo curso até 3 vezes, sendo aprovado quando obter média >= 70.0
# Definir as tabelas (entities) com seu respectivos atributos - definir os "constraints" e as chaves primárias e/ou estrangeiras

import os, sys, re, sqlite3

class Person:
    def __init__(self):
        self.first_name = input("Por favor, insira o *primeiro nome* da pessoa:\n")
        self.last_name = input("Por favor, insira o *último nome* da pessoa:\n")
        self.birth = input("Por favor, insira a *data de nascimento* da pessoa:\n")
        self.email = input("Por favor, insira o *e-mail* da pessoa:\n")
        cursor.execute("INSERT INTO Person (first_name,last_name,email,birth) VALUES (?,?,?,?)", (self.first_name, self.last_name, self.email, self.birth,))

    def is_student(self):
        pass

    def is_teacher(self):
        self.registration = input("Por favor, insira o *número de registro* do professor:\n")
        person_id = cursor.execute("SELECT last_insert_rowid()").fetchall()
        cursor.execute("INSERT INTO Teacher (person_id,registration) VALUES (?,?)", (person_id[0][0], self.registration,))


def print_full_table(table):
    cursor_head = db.execute(f'SELECT * FROM {table}') #cursos para pegar o cabecalho
    print([description[0] for description in cursor_head.description]) #imprimo o cabecalho
    print(cursor.execute(f'SELECT * FROM {table}').fetchall())

if __name__=="__main__":

    os.chdir(sys.path[0]) #seleciono o caminho atual como padrão
    address = os.path.join('files', 'university.db')

    db = sqlite3.connect(address) #Cria o bd se não existir
    cursor = db.cursor() #Cria um cursor para fazer as operações com o banco de dados
    cursor.execute("PRAGMA foreign_keys = ON").fetchall()

    ### SQL Tables ###

    #Person Table
    person_table = """CREATE TABLE IF NOT EXISTS Person (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR2(255),
    last_name VARCHAR2(255),
    email VARCHAR2(255),
    birth DATE);
    """
    #Student Table
    student_table = """CREATE TABLE IF NOT EXISTS Student (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL REFERENCES Person(id),
    registration INTEGER);
    """
    #Teacher Table
    teacher_table = """CREATE TABLE IF NOT EXISTS Teacher (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL REFERENCES Person(id),
    registration INTEGER);
    """
    #Course Table
    course_table = """CREATE TABLE IF NOT EXISTS Course (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR2(255),
    duration VARCHAR2(255),
    syllabus TEXT);
    """
    #Class Table
    class_table = """CREATE TABLE IF NOT EXISTS Class (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    schedule VARCHAR2(255),
    teacher_id INTEGER NOT NULL REFERENCES Teacher(id),
    course_id INTEGER NOT NULL REFERENCES Course(id));
    """
    #Grade Table
    grade_table = """CREATE TABLE IF NOT EXISTS Grade (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    value INTEGER,
    student_id INTEGER NOT NULL REFERENCES Student(id),
    teacher_id INTEGER NOT NULL REFERENCES Teacher(id),
    class_id INTEGER NOT NULL REFERENCES Class(id));
    """    
    cursor.execute(person_table) #Executa a tabela pessoa
    cursor.execute(teacher_table) #Executa a tabela professores

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
                    person_obj = Person()
                    db.commit() #executa as mudanças no bd
                    print(f"A pessoa {person_obj.first_name} {person_obj.last_name} foi cadastrada com sucesso.\n")                    
                    print_full_table('Person')
                elif resp == '2':
                    print(f"Resposta {resp}")
                    person_obj = Person()
                    person_obj.is_teacher()
                    db.commit() #executa as mudanças no bd
                    print(f"A pessoa {person_obj.first_name} {person_obj.last_name} foi cadastrada com sucesso.\n")
                    print_full_table('Teacher')
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
                print("'1' - Alunos cadastrados.")
                print("'2' - Professores cadastrados.")
                print("'3' - Cursos existentes.")
                print("'4' - Média dos alunos.")
                resp = input("")
                if resp == '1':
                    print(f"Resposta {resp}")
                    print_full_table('Person')
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
            	