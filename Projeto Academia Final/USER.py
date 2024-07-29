def user(mat):
    import BD
    import os
    import smtplib
    import email.message
    from tabulate import tabulate
    import TRATAMENTOS
    import sqlite3
    import regex

    choice = 0

    def title():
        print('-=-' * 7)
        print('-=- Espaço  ALUNO -=-')
        print('-=-' * 7)

    def infoAluno():
        print('Informações do aluno')
        print('Nome:',BD.usuarios[mat].nome)
        print('Email:',BD.usuarios[mat].email)
        print('Idade:',BD.usuarios[mat].idade)
        print('Faltas:',BD.usuarios[mat].faltas)

        print('Calorias necessarias:',BD.usuarios[mat].calorias)
        print('Peso:',BD.usuarios[mat].peso)
        print('Altura:',BD.usuarios[mat].altura)

    def choiceUSER():
        lista = ['Atualizar Dados', 'Justificar Falta','Mostrar Treino', 'Sair']
        for i in range(len(lista)):
            print(f'{i + 1}- {lista[i]}')
        c= input("O que deseja fazer? ")
        while c.isalpha() or not c.isalnum() or TRATAMENTOS.verificaNum(c):
            print("Inválido! Tente novamente.")
            c = input('O que deseja fazer? ')
        c= int(c)

        return c

    def atualizarDados():
        os.system('cls')
        title()
        banco= sqlite3.connect("Banco_de_Dados.db")
        cursor= banco.cursor()
        #TRATAMENTO ALTURA
        padrao_2= r'^[.,0-9]+$'
        altura = input("Digite a sua altura em CM: ").strip()
        while not regex.match(padrao_2, altura):
            print("Altura inválida. Use apenas pontos ou vírgulas.")
            altura = input("Digite a altura novamente: ").strip()
        altura= TRATAMENTOS.tratarNumero(altura)
        altura= int(altura)
        while altura<0:
            print("Altura inválida. Use apenas pontos ou vírgulas.")
            altura = input("Digite a altura novamente: ").strip()

        peso= input("Digite o seu peso em KG: ").strip()
        while not regex.match(padrao_2, peso):
            print("Peso inválido. Use apenas pontos ou vírgulas.")
            peso= input("Digite o peso novamente: ").strip()
        peso= TRATAMENTOS.commas(peso)
        peso= float(peso)

        idade= input('Insira sua idade: ').strip()
        #TRATAMENTO idade
        while idade.isalpha() or TRATAMENTOS.verificaNum(idade) or not idade.isalnum():
            idade= input("Inválido! Insira o sua idade novamente: ").strip()
        idade= int(idade)

        print("NÃO UTILIZE ESPAÇOS EM SUAS SENHAS!\nANOTE-A!")
        senha=input("Insira sua senha: ").strip()
        while senha =='' or len(senha)<8:
            print("A senha deve conter no mínimo 8 dígitos.")
            senha=input("Insira sua senha: ").strip()

        senha= TRATAMENTOS.tratarStrings(senha)

        sexo = input('Insira seu sexo (M/F/NB): ').strip()
        print(BD.usuarios[mat].idade)
        if sexo.upper() == 'M':
            tmb = (10*peso)+(6.25*altura)-(5*int(BD.usuarios[mat].idade))+5
            cal = tmb*1.24
        elif sexo.upper() == 'F':
            tmb = (10*peso)+(6.25*altura)-(5*int(BD.usuarios[mat].idade))-161
            cal = tmb*1.35
        else:
            tmb = (10*peso)+(6.25*altura)-(5*int(BD.usuarios[mat].idade))-78
            cal = tmb*1.29
        
        #REVISAR
        BD.usuarios[mat].altura = altura
        BD.usuarios[mat].peso = peso        
        BD.usuarios[mat].idade = idade
        BD.usuarios[mat].sexo = sexo
        BD.usuarios[mat].senha = senha
        BD.usuarios[mat].calorias = cal

        cursor.execute("UPDATE Alunos SET Calorias=?,Idade =?, Peso=?, Altura=?, Senha=? WHERE Matricula=?", (cal,idade,peso, altura, TRATAMENTOS.criptografador(senha), mat,))
        banco.commit()
        banco.close()

    def justificarFalta():
        os.system('cls')
        title()

        dia = input('Insira o dia que você deseja justificar a falta(dd/mm): ')
        just = input('Insira a justificativa da sua falta: ')

        try:

            corpo_email = f"""
                            <p>O aluno {BD.usuarios[mat].nome}, justificou sua falta do dia {dia} com a seguinte justificativa: </p>
                            <p>{just}</p>
                            """
            msg = email.message.Message()
            msg['Subject'] = f"Justificativa de falta {BD.usuarios[mat].nome}"
            msg['From'] = "projetoacademiacoel@gmail.com"
            msg['To'] = 'projetoacademiacoel@gmail.com'
            password = "mdekrwohqhvddtjd"
            msg.add_header("Content-Type", "text/html")
            msg.set_payload(corpo_email)

            s = smtplib.SMTP("smtp.gmail.com: 587")
            s.starttls()
            # Login Credenciais for sending the mail
            s.login(msg["From"], password)
            s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))
            input("E-mail enviado justificando sua falta.")
        except:
            print('Houve um erro ao enviar o email.')
            input('Confirme o email do destinatario e conexão da rede')

    def mostrarTreino():
        try:
            treinos = {}
            os.system('cls')
            title()
            treino = BD.lerTreinos(mat,treinos)

            print('Seu treino:')
            if len(treino) == 0:
                print('Você ainda não possui treinos, entre em contato com seus professores.')
            else:
                print(tabulate(treino, headers='keys', tablefmt='fancy_grid'))

            input()
        except:
            pass

    while choice != 4:
        os.system('cls')
        title()
        infoAluno()
        choice = choiceUSER()

        if choice == 1:
            atualizarDados()
        elif choice == 2:
            justificarFalta()
        elif choice == 3:
            mostrarTreino()