import string
import random
import re
import regex

def capitalizador(nome):
    separador= nome.split()
    capitalized_words= [palavras.capitalize() for palavras in separador]
    capitalized_aluno= ' '.join(capitalized_words)
    return capitalized_aluno

def tratarStrings(string):
    string_tratada= string.replace(" ", "")
    return string_tratada

def tratarNumero(num):
    num_tratado= num.replace(".", "").replace(",", "").replace(" ", "")
    return num_tratado

def commas(num):
    num_tratado= num.replace(",", ".").replace(" ", "")
    return num_tratado

def specials(texto):
    caracteres_especiais = set(string.punctuation) - set(',.')
    caracteres_tratados = ''
    for caractere in texto:
        if caractere not in caracteres_especiais:
            caracteres_tratados += caractere
    return caracteres_tratados

def verificaNum(texto):
    for caractere in texto:
        if caractere.isalpha():
            return True
    return False

def verificaNome(texto):
    for caractere in texto:
        if caractere.isnumeric():
            return True
        return False

def stringToFloat(string):

    a= tratarNumero(string)
    try:
        float(a)
        return True
    except ValueError:
        return False

def verificar_email(email):
    padrao = r'^\w+\.\w+(\.\w+)*@aluno\.uepb\.edu\.br$'
    if re.match(padrao, email):
        return True  
    return False

def processar_email(email):
    if '@' in email:
        a= verificar_email(email)
        if a==True:
            print("Email válido")
            novo_email= email
            return novo_email
        while a==False:
            novo_email =tratarStrings(input("Inválido! Insira o e-mail do aluno novamente: ").lower())
            a= verificar_email(novo_email)
    else:
        novo_email = f"{email}@aluno.uepb.edu.br"
        a= verificar_email(novo_email)
        if a==True:
            print("Email válido")
            return novo_email
        while a==False:
           novo_email =tratarStrings(input("Inválido! Insira o e-mail do aluno novamente: ").lower())
           if "@" in novo_email:
               a= verificar_email(novo_email)
           else: 
               novo_email= f"{novo_email}@aluno.uepb.edu.br"
               a= verificar_email(novo_email)
    return novo_email

def tratarTreinos(nome_treino):
    padrao = "^[a-zA-Z\sáÁàÀãÃâÂéÉêÊíÍóÓõÕôÔúÚçÇ]+$"

    if regex.match(padrao, nome_treino):
        return True
    return False

#criptografia
chave = '^!\$%&/()=?{[]}+~#-_.:,;<>|\\'

def criptografador(msg):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(msg,chave)])