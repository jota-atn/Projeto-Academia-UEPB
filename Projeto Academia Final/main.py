#Arquivos py
import os
import ADM
import USER
import BD

#Bibliotecas
from time import sleep
import smtplib
import email.message
import random
import sqlite3
import TRATAMENTOS

banco= sqlite3.connect("Banco_de_Dados.db")
cursor= banco.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Alunos(Matricula text, Senha text, Nome text, Email text, Idade integer, Faltas integer, Calorias real, Peso real, Altura integer)")

log = ''
# BD.BD()

BD.usuarios['admin1234'] = BD.adm()


def title(anim):
    titulo = 'Sistema Academia'
    if anim == 1:

        for i in range(len(titulo)):
            sleep(0.05)
            os.system('cls')
            print('-=-' * 8)
            print(f'-=- {titulo[:i + 1]:<16} -=-')
            print('-=-' * 8)
    else:
        print('-=-' * 8)
        print(f'-=- {titulo} -=-')
        print('-=-' * 8)

def recuperarSenha(mat):
    chave = ['A','B','C','D','E','0','1','2','3','4','5','6','7','8','9']

    code = ''

    for i in range(7):
        digit = chave[random.randint(0,14)]
        code = code+digit

    try:
        corpo_email = F"""
                <p> UMA SOLICITAÇÃO PARA ALTERAR SUA SENHA FOI FEITA. </p> 
                <p> CASO NÃO TENHA SIDO VOCÊ, CONTATE OS ADMINISTRADORES URGENTEMENTE! </p>
                <p> CASO CONTRÁRIO, IGNORE ESTA MENSAGEM. </p>
                <p> Seu código de acesso único: {code}. </p>
                <p> UTILIZE-O PARA ALTERAR SUA SENHA. </p>
                """
        msg = email.message.Message()
        msg['Subject'] = "Alteração de Senha"
        msg['From'] = "projetoacademiacoel@gmail.com"
        msg['To'] = BD.usuarios[mat].email
        password = "mdekrwohqhvddtjd"
        msg.add_header("Content-Type", "text/html")
        msg.set_payload(corpo_email)

        s = smtplib.SMTP("smtp.gmail.com: 587")
        s.starttls()
        # Login Credenciais for sending the mail
        s.login(msg["From"], password)
        s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))
        input("E-mail enviado.")
    

        codigo = input('Insira o codigo de acesso: ')
        while not codigo.isalnum():
            codigo= input("Inválido! Insira o código de acesso novamente: ")

        if codigo == code:
            BD.updateSenha(mat)
            input('Senha alterada com sucesso.')

        else:
            input('Codigo inválido')
    except:
        print('Houve um erro ao enviar o email.')
        input('Confirme o email do destinatario e conexão da rede')

def login():

    user = input('Insira o número da matrícula: ')

    while len(user)!= 9 or not user.isalnum():
        print('Matricula inválida')
        user= input("Insira o número da matrícula novamente: ")    

    if user == '000000000':
        print('Até mais!')

    elif user not in BD.usuarios:
        print('Não cadastrado')
        input()
    
    else:
        if BD.usuarios[user].permissao == 1:
            ADM.adm()
        else:
            cursor.execute(f"SELECT Senha FROM Alunos WHERE Matricula={user}")
            senha_aux= cursor.fetchall()

            senha = TRATAMENTOS.criptografador(input('Insira sua senha: '))

            if senha == senha_aux[0][0]:
                USER.user(user)

            else:
                input('Senha incorreta.')
                esc = input('Deseja recuperar a senha(s/n)? ').upper().strip()
                if esc == 'S':
                        recuperarSenha(user)  

    return user

os.system('cls')
title(1)
while log != '000000000':
    os.system('cls')
    title(0)
    log = login()