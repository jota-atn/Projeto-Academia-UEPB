import os
import BD
from time import sleep
from tabulate import tabulate

def adm():

    choice = 0

    def title(anim):
        titulo = 'Espaço ADM'
        if anim == 1:
            for i in range(len(titulo)):
                sleep(0.05)
                os.system('cls')
                print('-=-' * 6)
                print(f'-=- {titulo[:i + 1]:<10} -=-')
                print('-=-' * 6)

        else:
            print('-=-' * 6)
            print('-=- Espaço ADM -=-')
            print('-=-' * 6)

    def choiceADM():
        try:
            lista = ['Mostrar Alunos', 'Novo Aluno','Atualizar Aluno', 'Colocar falta em Aluno', 'Deletar Aluno','Ver Treino','Criar Treino','Deletar Treino', 'Sair']
            c = -1
            for i in range(len(lista)):
                sleep(0.05)
                print(f'{i + 1}- {lista[i]}')

            while 1 > c or len(lista) < c:
                c = int(input('O que deseja fazer? '))
            return c
        except:
            pass

    def mostrarAlunos():
        os.system('cls')
        title(0)

        x = 1
        lista = []
        for i in BD.usuarios:
            if BD.usuarios[i].permissao==0:
                #print(f'{x}-{i} -- {BD.usuarios[i].nome} -- {BD.usuarios[i].email} -- {BD.usuarios[i].faltas} faltas')
                lista.append([x,i, BD.usuarios[i].nome, BD.usuarios[i].email, BD.usuarios[i].faltas])
            x += 1
        print('Tabela dos alunos:')
        print(tabulate(lista, headers=['','Matrícula','Nome do Aluno','Email', 'Faltas'], tablefmt='fancy_grid'))
        input()

    def verTreino():
        mat = input('Insira a matricula do aluno: ')
        while len(mat)!= 9 or not mat.isdigit():
            print("Inválido! Tente novamente com uma matrícula válida.")
            mat = input('Insira a matricula do aluno a ser deletado: ')

        try:
            treinos = {}
            os.system('cls')
            title(2)
            treino = BD.lerTreinos(mat, treinos)
            print(f'Treino do aluno {BD.usuarios[mat].nome}:')
            if len(treino) == 0:
                print('Você ainda não possui treinos, entre em contato com seus professores.')
            else:
                print(tabulate(treino, headers='keys', tablefmt='fancy_grid'))

            input()
        except:
            pass

    os.system('cls')
    title(1)
    while choice != 9:
        os.system('cls')
        title(0)
        choice = choiceADM()

        if choice == 1:
            mostrarAlunos()
        elif choice ==2:
            os.system('cls')
            title(0)
            BD.novoAluno()
        elif choice == 3:
            os.system('cls')
            title(0)
            BD.updateAluno()
        elif choice == 4:
            os.system('cls')
            title(0)
            BD.faltaAluno()
        elif choice == 5:
            os.system('cls')
            title(0)
            BD.removeAluno(2)
        elif choice == 6:        
            verTreino()
        elif choice == 7:
            os.system('cls')
            title(0)
            BD.criarTreino()
        elif choice == 8:
            os.system('cls')
            title(0)
            mat = input('Insira a matricula do aluno a ser deletado: ')
            #TRATAMENTO MATRICULA
            while len(mat)!= 9 or not mat.isdigit():
                print("Inválido! Tente novamente com uma matrícula válida.")
                mat = input('Insira a matricula do aluno a ser deletado: ')
            BD.removerTabela(mat)