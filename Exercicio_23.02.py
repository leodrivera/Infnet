
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
        self.registration = input("Por favor, insira o *número de registro* do aluno:\n")
        person_id = cursor.execute("SELECT last_insert_rowid() FROM Student").fetchall()
        cursor.execute("INSERT INTO Student (person_id,registration) VALUES (?,?)", (person_id[0][0], self.registration,))

    def is_teacher(self):
        self.registration = input("Por favor, insira o *número de registro* do professor:\n")
        person_id = cursor.execute("SELECT last_insert_rowid()").fetchall()
        cursor.execute("INSERT INTO Teacher (person_id,registration) VALUES (?,?)", (person_id[0][0], self.registration,))


def print_full_table(table, cond='table'):
    if cond == 'table':
        cursor_head_var = f'SELECT * FROM {table}'
    elif cond == 'join':
        cursor_head_var = table
    cursor_head = db.execute(cursor_head_var) #cursor para pegar o cabecalho        
    print([description[0] for description in cursor_head.description]) #imprimo o cabecalho
    print(cursor.execute(cursor_head_var).fetchall())

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
    value DECIMAL(4, 2),
    student_id INTEGER NOT NULL REFERENCES Student(id),
    class_id INTEGER NOT NULL REFERENCES Class(id));
    """    
    cursor.execute(person_table) #Executa a tabela pessoa
    cursor.execute(student_table) #Executa a tabela estudante
    cursor.execute(teacher_table) #Executa a tabela professores
    cursor.execute(course_table) #Executa a tabela curso
    cursor.execute(class_table) #Executa a tabela turma
    cursor.execute(grade_table) #Executa a tabela nota

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
                print("'4' - Turma.")
                print("'5' - Alunos na turma e sua nota.")
                resp = input("")
                if resp == '1':
                    print(f"Resposta {resp}")
                    person_obj = Person()
                    person_obj.is_student()
                    db.commit() #executa as mudanças no bd
                    print(f"A pessoa {person_obj.first_name} {person_obj.last_name} foi cadastrada com sucesso.\n")                    
                    print_full_table('Student','table')
                elif resp == '2':
                    print(f"Resposta {resp}")
                    person_obj = Person()
                    person_obj.is_teacher() #Método para inserir os dados adicionais de professor
                    db.commit() #executa as mudanças no bd
                    print(f"A pessoa {person_obj.first_name} {person_obj.last_name} foi cadastrada com sucesso.\n")
                    print_full_table('Teacher','table')
                elif resp == '3':
                    print(f"Resposta {resp}")
                    name = input("Por favor, insira o *nome* do Curso:\n")
                    duration = input("Por favor, insira a *duração* do curso:\n")
                    syllabus = input("Por favor, insira a *ementa* do curso:\n")
                    cursor.execute("INSERT INTO Course (name,duration,syllabus) VALUES (?,?,?)", (name, duration, syllabus,))
                    db.commit() #executa as mudanças no bd
                    print(f"O curso {name} foi cadastrado com sucesso.\n")
                elif resp == '4':
                    print(f"Resposta {resp}")
                    schedule = input("Por favor, insira o *horário* das aulas da turma:\n")
                    teacher_id = input("Por favor, insira o *id do professor* da turma:\n")
                    course_id = input("Por favor, insira o *id do do curso* relativo à turma:\n")
                    try:
                        cursor.execute("INSERT INTO Class (schedule,teacher_id,course_id) VALUES (?,?,?)", (schedule, teacher_id, course_id,))
                        db.commit() #executa as mudanças no bd
                        id_class = cursor.execute("SELECT last_insert_rowid()").fetchall()
                        print(f"A turma {id_class[0][0]} foi cadastrada com sucesso.\n")
                    except sqlite3.IntegrityError:
                        print("Verifique se você inseriu os ids corretamente.")
                elif resp == '5':
                    print(f"Resposta {resp}")
                    student_id = input("Por favor, insira o *id do aluno*:\n")
                    class_id = input("Por favor, insira o *id da turma*:\n")
                    try:
                        course_id_atual = cursor.execute('SELECT Co.id FROM Grade G INNER JOIN Class Cl ON (G.student_id = ?) AND (G.class_id = ?) AND (G.class_id = Cl.id) '
                        'INNER JOIN Course Co ON (Co.id = Cl.course_id)',(student_id,class_id,)).fetchall()
                        if course_id_atual != []:
                            student_tries = cursor.execute('SELECT COUNT(G.student_id) FROM Grade G INNER JOIN Class Cl ON (G.student_id = ?) AND (G.class_id = Cl.id) '
                            'INNER JOIN Course Co ON (Cl.course_id = Co.id) AND (Co.id = ?)',(student_id,course_id_atual[0][0],)).fetchall()
                            ##Forma alternativa##
                            #course_id_atual = cursor.execute('SELECT Co.id FROM Grade G, Class Cl, Course Co WHERE (G.student_id = ?) AND (G.class_id = ?) ' 
                            #'AND (G.class_id = Cl.id) AND (Co.id = Cl.course_id)'(student_id,class_id,)).fetchall()
                            #student_tries = cursor.execute('SELECT COUNT(G.student_id) FROM Grade G, Class Cl, Course Co WHERE (G.student_id = ?) AND (G.class_id = Cl.id) AND '
                            #'(Cl.course_id = Co.id) AND (Co.id = ?)',(student_id,course_id_atual[0][0],)).fetchall()
                            if student_tries[0][0] > 3:
                                student_name = cursor.execute('SELECT P.first_name, P.last_name FROM Student S INNER JOIN Person P ON (S.person_id = P.id) AND (S.id = ?)',(student_id,)).fetchall()
                                print(f"O aluno {student_name[0][0]} {student_name[0][1]} de id {student_id} já realizou o curso por 3 vezes.")
                        else:
                            value = input("Por favor, insira a *nota do aluno*:\n")
                            cursor.execute("INSERT INTO Grade (student_id,class_id,value) VALUES (?,?,?)", (student_id, class_id, value,))
                            db.commit() #executa as mudanças no bd
                            student_name = cursor.execute('SELECT P.first_name, P.last_name FROM Student S INNER JOIN Person P ON (S.person_id = P.id) '
                            'INNER JOIN Grade G ON (S.id = G.student_id) ORDER BY G.id DESC').fetchall()
                            print(f"O aluno {student_name[0][0]} {student_name[0][1]} teve sua nota cadastrada com sucesso.\n")
                    except NameError or sqlite3.IntegrityError:
                        print("ATENÇÃO! Verifique se você inseriu os ids corretamente.\n")
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
                print("'4' - Turmas existentes.")
                print("'5' - Nota dos alunos.")
                resp = input("")
                if resp == '1':
                    print(f"Resposta {resp}")
                    sql_inner_join = ('SELECT S.id, P.first_name, P.last_name, P.email, P.birth, S.registration '
                    'FROM Person P INNER JOIN Student S ON P.id=S.person_id')
                    print_full_table(sql_inner_join,'join')
                elif resp == '2':
                    print(f"Resposta {resp}")
                    sql_inner_join = ('SELECT T.id, P.first_name, P.last_name, P.email, P.birth, T.registration '
                    'FROM Person P INNER JOIN Teacher T ON P.id=T.person_id')
                    print_full_table(sql_inner_join,'join')
                elif resp == '3':
                    print(f"Resposta {resp}")
                    print_full_table('Course','table')
                elif resp == '4':
                    print(f"Resposta {resp}")
                    print_full_table('Class','table')
                elif resp == '5':
                    print(f"Resposta {resp}")
                    print_full_table('Grade','table')
                    print('')                
                    sql_inner_join_student = ('SELECT P.first_name, P.last_name, G.value, G.class_id FROM Student S INNER JOIN Person P ON (S.person_id = P.id) '
                    'INNER JOIN Grade G ON (S.id = G.student_id)')
                    sql_join_teacher = ('SELECT P.first_name, P.Last_name, Co.name, Cl.id as cl_id FROM Teacher T, Person P, Course Co, Class Cl WHERE '
                    '(Cl.teacher_id = T.id) AND (P.id = T.person_id) AND (Co.id = Cl.course_id)')
                    sql_join_total_1 = ('SELECT t1.first_name as "Student First Name", t1.last_name as "Student Last Name", t1.value as Grade, '
                    f't2.first_name as "Teacher First Name", t2.Last_name as "Teacher Last Name", t2.name as "Course Name" FROM ({sql_inner_join_student}) t1 '
                    f'INNER JOIN ({sql_join_teacher}) t2 ON (t1.class_id = t2.cl_id)')
                    print_full_table(sql_join_total_1,'join')
                    print('')
                    sql_join_total_2 = ('SELECT t1.first_name as "Student First Name", t1.last_name as "Student Last Name", SUM(t1.value)/COUNT(t1.value) as '
                    'Grade, (CASE WHEN SUM(t1.value)/COUNT(t1.value) >= 70 THEN "APPROVED" ELSE "DISAPPROVED" END) as Result, t2.name as "Course Name" '
                    f'FROM ({sql_inner_join_student}) t1 INNER JOIN ({sql_join_teacher}) t2 ON (t1.class_id = t2.cl_id) GROUP BY t2.name')
                    print_full_table(sql_join_total_2,'join')
                else:
                    print("Saindo do módulo consulta.")
                    break
        else:
            print("Saindo do programa.")
            break
    db.close() #Fecha a conexão com o bd
            	