# Modelar um sistema de gerenciamento de banco de dados de alunos para Universidades Com as seguintes considerações:

# Você deverá cadastrar as seguintes informações de cada profissional da Universidade (Alunos e Professores):
# Primeiro nome; Sobrenome; Data de nascimento ; email do aluno
# Cada aluno poderá se matricular em um determinado curso dado por um determinado professor
# Cada aluno poderá realizar o mesmo curso até 3 vezes, sendo aprovado quando obter média >= 70.0
# Definir as tabelas (entities) com seu respectivos atributos - definir os "constraints" e as chaves primárias e/ou estrangeiras

import os, sys, re, sqlite3

class Person():
    def __init__(self):
        self.first_name = input("Por favor, insira o *primeiro nome* da pessoa:\n")
        self.last_name = input("Por favor, insira o *último nome* da pessoa:\n")
        self.birth = input("Por favor, insira a *data de nascimento* da pessoa, no formato dd/mm/yyyy:\n")
        self.birth = check.birth(self.birth) # função para checar se a data está no formato correto
        self.email = input("Por favor, insira o *e-mail* da pessoa:\n")
        self.email = check.email(self.email) # função para checar se a data está no formato correto

    def table_insert(self):
        cursor.execute("INSERT INTO Person (first_name,last_name,email,birth) VALUES (?,?,?,?)", (self.first_name, self.last_name, self.email, self.birth,))

class Teacher(Person):
    def __init__(self):
        super().__init__()
        super().table_insert()
        self.registration = input("Por favor, insira o *número de registro* do professor (5 digitos):\n")
        self.person_id = cursor.execute("SELECT last_insert_rowid() FROM Person").fetchall()

    def table_insert(self):
        cursor.execute("INSERT INTO Teacher (person_id,registration) VALUES (?,?)", (self.person_id[0][0], self.registration,))

class Student(Person):
    def __init__(self):
        super().__init__()
        super().table_insert()
        self.registration = input("Por favor, insira o *número de registro* do aluno (5 dígitos):\n")
        self.person_id = cursor.execute("SELECT last_insert_rowid() FROM Person").fetchall()

    def table_insert(self):
        cursor.execute("INSERT INTO Student (person_id,registration) VALUES (?,?)", (self.person_id[0][0], self.registration,))

class Course:
    def __init__(self):
        self.name = input("Por favor, insira o *nome* do Curso:\n")
        self.duration = input("Por favor, insira a *duração* do curso, em meses:\n")
        self.duration = check.duration(self.duration)
        self.syllabus = input("Por favor, insira a *ementa* do curso:\n")

    def table_insert(self):
        cursor.execute("INSERT INTO Course (name,duration,syllabus) VALUES (?,?,?)", (self.name, self.duration, self.syllabus,))

class Class(Course):
    def __init__(self):
        self.schedule = input("Por favor, insira o *horário* das aulas da turma:\n")
        self.teacher_id = input("Por favor, insira o *id do professor* da turma:\n")
        self.teacher_id = check.id(self.teacher_id)
        self.course_id = input("Por favor, insira o *id do do curso* relativo à turma:\n")
        self.course_id = check.id(self.course_id)

    def table_insert(self):
        try:
            cursor.execute("INSERT INTO Class (schedule,teacher_id,course_id) VALUES (?,?,?)", (self.schedule, self.teacher_id, self.course_id,))
            self.id_class = cursor.execute("SELECT last_insert_rowid() FROM Class").fetchall()  #O número da turma é o seu próprio ID
            return True

        except sqlite3.IntegrityError:
            print("Verifique se você inseriu os ids corretamente e tente novamente.\n")
            return False

class Check:
    def __regex_check(self):
        result = re.search(self.regex, self.text)
        while not result:
            self.text = input(self.message)
            result = re.search(self.regex, self.text)
        return self.text

    def registration(self, registration):
        self.text = registration
        self.regex = '^\d{5}$' # para detectar 5 dígitos
        self.message = "O *número de registro* deve conter 5 dígitos:\n"
        return self.__regex_check()

    def birth(self, date):
        self.text = date
        self.regex = '^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/\d{4}$' # para detectar dd/mm/aaaa
        self.message = "A *data de nascimento* deve estar no formato dd/mm/yyyy:\n"
        return self.__regex_check()

    def email(self, email):
        self.text = email
        self.regex = '^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]+)$' # para detectar e-mail válido
        self.message = "Por favor, insira um e-mail válido:\n"
        return self.__regex_check()

            
    def duration(self, duration):
        self.text = duration
        self.regex = '^\d+$' # para detectar dígitos
        self.message = "Por favor, insira somente o número de meses:\n"
        return self.__regex_check()

    def id(self, id):
        self.text = id
        self.regex = '^\d+$' # para detectar dígitos
        self.message = "O *id* deve conter somente dígitos :\n"
        return self.__regex_check()

def print_full_table(table, cond='table'):
    if cond == 'table':
        cursor_head_var = f'SELECT * FROM {table}'
    elif cond == 'join':
        cursor_head_var = table
    cursor_head = db.execute(cursor_head_var) #cursor para pegar o cabecalho        
    print([description[0] for description in cursor_head.description]) #imprimo o cabecalho
    print(cursor.execute(cursor_head_var).fetchall())

if __name__=="__main__":
    check = Check() #Crio um objeto para a classe Check
    
    os.chdir(sys.path[0]) #seleciono o caminho atual como padrão

    #Verifico se existe a pasta files. Se não existir, eu crio.
    if not os.path.isdir("files"):
        os.mkdir("files")
    
    address = os.path.join("files", 'university.db')

    db = sqlite3.connect(address) #Cria o bd se não existir
    cursor = db.cursor() #Cria um cursor para fazer as operações com o banco de dados
    cursor.execute("PRAGMA foreign_keys = ON").fetchall()

    ### SQL Tables ###

    #Person Table
    person_table = """CREATE TABLE IF NOT EXISTS Person (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR2(255),
    last_name VARCHAR2(255),
    email VARCHAR2(255) UNIQUE,
    birth DATE);
    """
    #Student Table
    student_table = """CREATE TABLE IF NOT EXISTS Student (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL REFERENCES Person(id),
    registration INTEGER UNIQUE);
    """
    #Teacher Table
    teacher_table = """CREATE TABLE IF NOT EXISTS Teacher (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL REFERENCES Person(id),
    registration INTEGER UNIQUE);
    """
    #Course Table
    course_table = """CREATE TABLE IF NOT EXISTS Course (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR2(255) UNIQUE,
    duration INTEGER,
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
                    student_obj = Student()
                    student_obj.table_insert()
                    db.commit() #executa as mudanças no bd
                    print(f"A pessoa {student_obj.first_name} {student_obj.last_name} foi cadastrada com sucesso.\n")                    
                    print_full_table('Student','table')

                elif resp == '2':
                    print(f"Resposta {resp}")
                    teacher_obj = Teacher()
                    teacher_obj.table_insert()
                    db.commit() #executa as mudanças no bd
                    print(f"A pessoa {teacher_obj.first_name} {teacher_obj.last_name} foi cadastrada com sucesso.\n")
                    print_full_table('Teacher','table')

                elif resp == '3':
                    print(f"Resposta {resp}")
                    course_obj = Course()
                    course_obj.table_insert()
                    db.commit() #executa as mudanças no bd
                    print(f"O curso {course_obj.name} foi cadastrado com sucesso.\n")
                    print_full_table('Course','table')

                elif resp == '4':
                    print(f"Resposta {resp}")
                    class_obj = Class()
                    result = class_obj.table_insert()
                    if result: #se tiver ok
                        db.commit() #executa as mudanças no bd
                        print(f"A turma {class_obj.id_class[0][0]} foi cadastrada com sucesso.\n")
                        print_full_table('Class','table')

                elif resp == '5':
                    print(f"Resposta {resp}")
                    student_id = input("Por favor, insira o *id do aluno*:\n")
                    student_id = check.id(student_id)
                    class_id = input("Por favor, insira o *id da turma*:\n")
                    class_id = check.id(class_id)
                    student_name = cursor.execute('SELECT P.first_name, P.last_name FROM Student S INNER JOIN Person P ON (S.person_id = P.id) AND (S.id = ?)',(student_id,)).fetchall()
                    exceeded = False

                    #ID do curso relativo a turma a qual está se querendo adicionar
                    course_id_atual = cursor.execute('SELECT Co.id FROM Class Cl INNER JOIN Course Co ON (Co.id = Cl.course_id) AND (Cl.id = ?)',(class_id,)).fetchall()

                    #Método para ver se o aluno já está cadastrado na turma
                    val = cursor.execute(f'SELECT G.student_id, G.class_id FROM Grade G WHERE (student_id = ?) AND (class_id = ?)',(student_id,class_id,)).fetchall()

                    #Método para ver quantas vezes o aluno já fez o curso relativo à turma
                    student_tries = cursor.execute('SELECT COUNT(*) FROM Grade G INNER JOIN Class Cl ON (G.student_id = ?) AND (G.class_id = Cl.id) '
                    'INNER JOIN Course Co ON (Co.id = Cl.course_id) AND (Co.id = ?) GROUP BY Co.id',(student_id, course_id_atual[0][0])).fetchall()
                    
                    if student_tries == []:
                        student_tries = [(0,)]

                    if student_tries[0][0] > 2:
                        print(f"O aluno {student_name[0][0]} {student_name[0][1]}, de id {student_id}, já realizou o curso de id {course_id_atual[0][0]} por 3 vezes.\n")
                        exceeded = True                           

                    if val != []:
                        print(f"O aluno {student_name[0][0]} {student_name[0][1]}, de id {student_id}, já foi cadastrado na turma {class_id}.\n")
                        exceeded = True
                    try: 
                        if not exceeded:
                            value = input("Por favor, insira a *nota do aluno*, variando de 0 a 100:\n")
                            cursor.execute("INSERT INTO Grade (student_id,class_id,value) VALUES (?,?,?)", (student_id, class_id, value,))
                            db.commit() #executa as mudanças no bd
                            print(f"O aluno {student_name[0][0]} {student_name[0][1]} teve sua nota cadastrada com sucesso.\n")

                    except sqlite3.IntegrityError:
                        print(f"ATENÇÃO! Verifique se você inseriu os ids corretamente.\n")

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

                    #Pego o estudante que consta em 'Person', 'Student' e 'Grade', sua nota e o ID da turma
                    sql_inner_join_student = ('SELECT P.id, P.first_name, P.last_name, G.value, G.class_id FROM Student S INNER JOIN Person P ON (S.person_id = P.id) '
                    'INNER JOIN Grade G ON (S.id = G.student_id)')

                    #Pego o professor que consta em 'Person', 'Teacher' e 'Classe' e o nome do curso
                    sql_join_teacher = ('SELECT P.first_name, P.Last_name, Co.name, Cl.id as cl_id FROM Teacher T, Person P, Course Co, Class Cl WHERE '
                    '(Cl.teacher_id = T.id) AND (P.id = T.person_id) AND (Co.id = Cl.course_id)')

                    sql_join_total_1 = ('SELECT t1.first_name as "Student First Name", t1.last_name as "Student Last Name", t1.value as Grade, '
                    f't2.first_name as "Teacher First Name", t2.Last_name as "Teacher Last Name", t2.name as "Course Name" FROM ({sql_inner_join_student}) t1 '
                    f'INNER JOIN ({sql_join_teacher}) t2 ON (t1.class_id = t2.cl_id)')
                    print('### Nota dos alunos por turma ###')
                    print_full_table(sql_join_total_1,'join')
                    
                    sql_join_total_2 = ('SELECT t1.first_name as "Student First Name", t1.last_name as "Student Last Name", SUM(t1.value)/COUNT(t1.value) as '
                    'Grade, (CASE WHEN SUM(t1.value)/COUNT(t1.value) >= 70 THEN "APPROVED" ELSE "DISAPPROVED" END) as Result, t2.name as "Course Name" '
                    f'FROM ({sql_inner_join_student}) t1 INNER JOIN ({sql_join_teacher}) t2 ON (t1.class_id = t2.cl_id) GROUP BY t1.id, t2.name')
                    print('\n### Nota dos alunos consolidada ###')
                    print_full_table(sql_join_total_2,'join')

                else:
                    print("Saindo do módulo consulta.")
                    break
        else:
            print("Saindo do programa.")
            break
        
    db.close() #Fecha a conexão com o bd