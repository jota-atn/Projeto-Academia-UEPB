import sqlite3
import smtplib
import email.message
import TRATAMENTOS
import time

banco= sqlite3.connect("Banco_de_Dados.db")
cursor= banco.cursor()

usuarios = {}

class adm():
    permissao = 1

class user():
    permissao = 0
    nome = ''
    email = ''
    idade = 0
    faltas = 0
    calorias = 0
    peso = 0
    altura = 0
    sexo = 'M'


    

def lerBD():
    cursor.execute("SELECT * FROM Alunos")
    alunos = cursor.fetchall()

    for i in range(len(alunos)):
        usuarios[alunos[i][0]] = user()
    x = 0
    for i in usuarios:
        usuarios[i].nome = alunos[x][2]
        usuarios[i].email = alunos[x][3]
        usuarios[i].idade = alunos[x][4]
        usuarios[i].faltas = alunos[x][5]
        usuarios[i].calorias = alunos[x][6]
        usuarios[i].peso = alunos[x][7]
        usuarios[i].altura = alunos[x][8]
        x+=1

def novoAluno():
    #COLOCANDO DADOS NO BANCO
    banco= sqlite3.connect("Banco_de_Dados.db")
    cursor= banco.cursor()
    matricula= input("Insira o número da matrícula: ")
    #TRATAMENTO MATRICULA
    while len(matricula)!= 9 or not matricula.isdigit():
        print("Inválido! Tente novamente com uma matrícula válida.")
        matricula= input("Insira o número da matrícula novamente: ")
    if matricula not in usuarios:
        nome= input("Insira o nome do aluno: ").lower()
        #TRATAMENTO NOME
        while nome.isnumeric() or not nome.isalnum:
            nome= input("Inválido! Insira o nome do aluno novamente: ")
        nome= TRATAMENTOS.capitalizador(nome)

        email = TRATAMENTOS.tratarStrings(input("Insira o e-mail do aluno: ").lower())
        email = TRATAMENTOS.processar_email(email)
        idade = input("Insira a idade do aluno: ")
        #TRATAMENTO IDADE
        while idade.isalpha() or not idade.isalnum() or TRATAMENTOS.verificaNum(idade):
            print("Inválido! Tente novamente com uma idade válida.")
            idade = input("Insira a idade do aluno novamente: ")
        idade= int(idade)

        faltas= 0
        peso= 0
        cal= 0
        altura= 0
        senha= matricula
        cursor.execute(
            ("INSERT INTO Alunos VALUES(?,?,?,?,?,?,?,?,?)"), (matricula, TRATAMENTOS.criptografador(senha), nome, email, str(idade), str(faltas), str(cal), str(peso), str(altura),))
        cursor.execute(f'CREATE TABLE IF NOT EXISTS Treino{matricula}(Dia text, Treino text)')
        
        banco.commit()

        usuarios[matricula] = user()

        usuarios[matricula].nome = nome
        usuarios[matricula].email = email
        usuarios[matricula].idade = idade
        usuarios[matricula].faltas = faltas

        
    else:
        input('Matricula ja cadastrada')

def removeAluno(tipo):
    banco= sqlite3.connect("Banco_de_Dados.db")
    cursor= banco.cursor()
    try:
        if tipo == 1:
            try:
                cursor.execute('SELECT Matricula FROM Alunos WHERE Faltas> 2')
                mat = cursor.fetchall()[0][0]
                removerTabela(mat)
                banco = sqlite3.connect('Banco_de_Dados.db')
                cursor_aux = banco.cursor()
                cursor_aux.execute("DELETE FROM Alunos WHERE Faltas> 2")
                del usuarios[mat]
                banco.commit()
                banco.close()
                print("Aluno removido com sucesso.")
            except sqlite3.Error as erro:
                print(f"Houve um erro ao remover o aluno.\nErro: '{erro}'.")

        elif tipo == 2:
            mat_remove = input('Insira a matricula do aluno a ser deletado: ')
            #TRATAMENTO MATRICULA
            while len(mat_remove)!= 9 or not mat_remove.isdigit():
                print("Inválido! Tente novamente com uma matrícula válida.")
                mat_remove = input('Insira a matricula do aluno a ser deletado: ')
            try:
                cursor.execute(
                    ("DELETE FROM Alunos WHERE Matricula= ?"), (mat_remove,))
                banco.commit()
                banco.close()

                del usuarios[mat_remove]
                removerTabela(mat_remove)

                print("Aluno removido com sucesso.")
            except sqlite3.Error as erro:
                print(f"Houve um erro ao remover o aluno.\nErro: '{erro}'.")
        
                
        
    except:
        pass

def updateAluno():
    banco= sqlite3.connect("Banco_de_Dados.db")
    cursor= banco.cursor()
    mat = input('Insira a matrícula do aluno: ')
    while len(mat)!= 9 or not mat.isdigit():
                print("Inválido! Tente novamente com uma matrícula válida.")
                mat = input('Insira a matricula do aluno a ser deletado: ')
    if mat in usuarios:
        nome= input("Insira o nome do aluno: ").lower()
        #TRATAMENTO NOME
        while nome.isnumeric() or not nome.isalnum:
            nome= input("Inválido! Insira o nome do aluno novamente: ")
        nome= TRATAMENTOS.capitalizador(nome)

        email = TRATAMENTOS.tratarStrings(input("Insira o e-mail do aluno: ").lower())
        email = TRATAMENTOS.processar_email(email)
        cursor.execute(
            ("UPDATE Alunos SET Nome=?, Email=? WHERE Matricula=?"), (nome, email, mat,))
        usuarios[mat].nome = nome
        usuarios[mat].email = email
        
        banco.commit()
        banco.close()

def updateSenha(mat):
    banco= sqlite3.connect("Banco_de_Dados.db")
    cursor= banco.cursor()
    senha_nova= input("Insira a nova senha do aluno: ")
    cursor.execute(
        ("UPDATE Alunos SET Senha=? WHERE Matricula=?"), (TRATAMENTOS.criptografador(senha_nova), mat,))
    banco.commit()
    banco.close()

def enviar_email(mat, type, faltas):
    try:
        if type == 1:
            corpo_email = F"""
                <p> VOCÊ POSSUI {faltas} FALTAS </p>
                <p> QUANDO A SUA QUANTIDADE DE FALTAS ATINGIR 3, VOCÊ SERÁ DESLIGADO DO PROGRAMA. </p>
                """
            msg = email.message.Message()
            msg['Subject'] = "Aviso de faltas"
            msg['From'] = "projetoacademiacoel@gmail.com"
            msg['To'] = usuarios[mat].email
            password = "mdekrwohqhvddtjd"
            msg.add_header("Content-Type", "text/html")
            msg.set_payload(corpo_email)

            s = smtplib.SMTP("smtp.gmail.com: 587")
            s.starttls()
            # Login Credenciais for sending the mail
            s.login(msg["From"], password)
            s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))
            input("E-mail avisando sobre as faltas foi enviado.")

        elif type == 2:
            corpo_email = F"""
                    <p> VOCÊ POSSUI {faltas} FALTAS </p>
                    <p> COMO FOI AVISADO ANTERIOMENTE, VOCÊ SERÁ DESLIGADO DO PROGRAMA.</p>
                    """
            msg = email.message.Message()
            msg['Subject'] = "Aviso de desligamento."
            msg['From'] = "projetoacademiacoel@gmail.com"
            msg['To'] = usuarios[mat].email
            password = "mdekrwohqhvddtjd"
            msg.add_header("Content-Type", "text/html")
            msg.set_payload(corpo_email)

            s = smtplib.SMTP("smtp.gmail.com: 587")
            s.starttls()
            # Login Credenciais for sending the mail
            s.login(msg["From"], password)
            s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))
            input("E-mail avisando sobre o desligamento foi enviado.")
    except:
        print('Houve um erro ao enviar o email.')
        input('Confirme o email do destinatario e conexão da rede')

def faltaAluno():
    banco= sqlite3.connect("Banco_de_Dados.db")
    cursor= banco.cursor()

    mat = input('Insira a matricula do aluno: ')
    #TRATAMENTO DA MATRÍCULA
    while len(mat)!= 9 or not mat.isnumeric():
        print("Inválido! Tente novamente com uma matrícula válida.")
        mat= input("Inválido! Insira a matrícula do aluno novamente: ")

    faltas= input('Insira a quantidade de faltas desse aluno: ')
    #TRATAMENTO DAS FALTAS
    while not faltas.isalnum() or faltas.isalpha() or TRATAMENTOS.verificaNum(faltas) or 3<int(faltas):
        faltas= input('Inválido! Insira a quantidade de faltas desse aluno novamente: ')
    faltas= int(faltas)

    cursor.execute(f"UPDATE Alunos SET Faltas= {faltas} WHERE Matricula= {mat}")
    banco.commit()

    if mat not in usuarios:
        print("Aluno não cadastrado. ")
        time.sleep(1)
        print("Voltando ao menu...")
        time.sleep(2)
        return
    else:
        usuarios[mat].faltas = faltas

        if faltas <=2:
            enviar_email(mat, 1, faltas)
        else:
            enviar_email(mat, 2, faltas)
            removeAluno(1)

def removerTabela(mat):
    banco= sqlite3.connect("Banco_de_Dados.db")
    cursor= banco.cursor()
    cursor.execute(f"DROP Table IF EXISTS Treino{mat}")
    banco.commit()
    banco.close()

def criarTreino():
    mat = input('Insira a matricula do aluno: ')
    while len(mat)!= 9 or not mat.isdigit():
        print("Inválido! Tente novamente com uma matrícula válida.")
        mat = input('Insira a matricula do aluno a ser deletado: ')

    dias_semana = ['Segunda', 'Terca', 'Quarta', 'Quinta']
    banco= sqlite3.connect("Banco_de_Dados.db")
    cursor= banco.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS Treino{mat}(Dia text, Treino text)")

    for dia in dias_semana:
        nTreinos= input(f'Quantidade de treinos para {dia}: ')

        #TRATAMENTO NTREINOS
        while nTreinos.isalpha() or not nTreinos.isalnum() or TRATAMENTOS.verificaNum(nTreinos):
            nTreinos= input(f'Inválido! Insira a quantidade de treinos para {dia} novamente: ')
        nTreinos= int(nTreinos)

        for i in range(nTreinos):
            print("NÃO UTILIZE ESPAÇOS")
            treino= input(f'Informe o treino {i+1}: ').lower().strip()
            a = TRATAMENTOS.tratarTreinos(treino)

            while a==False:
                treino= input(f'Informe o treino {i+1} novamente: ').lower().strip()
                a = TRATAMENTOS.tratarTreinos(treino)

            treino= TRATAMENTOS.capitalizador(treino)
            cursor.execute(f"INSERT INTO Treino{mat} (dia, treino) VALUES (?, ?)", (dia, treino))
            banco.commit()

    banco.close()

treinos= {}
def lerTreinos(matricula, treinos):
    try:
        banco= sqlite3.connect("Banco_de_Dados.db")
        cursor= banco.cursor()
        cursor.execute(f"SELECT * FROM Treino{matricula}")
        fichas= cursor.fetchall()
        for ficha in fichas:
            dia= ficha[0]
            treino= ficha[1]
            
            if dia in treinos:
                treinos[dia].append(treino)
            else:
                treinos[dia] = [treino]
        return treinos
    except:
        input('Você ainda não possui treinos, entre em contato com seus professores.')