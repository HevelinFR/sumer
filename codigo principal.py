#!/usr/bin/env python3
 # -*- coding: utf-8 -*-

'''Desenvolvedores: Hevelin de Jesus Freitas

Sistema de gerenciamento de livros
'''


import mysql.connector
import time
import os
import sys
from PySide2.QtUiTools import  QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QMainWindow
from PySide2.QtCore import QFile
from PySide2 import QtGui
from PySide2 import QtCore



meu_db = ("biblioteca",)

#conecta o python com o banco -------------------------------------------------
def conecta_db(db = None):

    if db == None:

        banco = mysql.connector.connect( #chamar conexão
                host = "localhost",
                user = "root",
                passwd = ""
                    )

        return banco

    else:
        banco = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = db
            )

        return banco

#Testar se existe um banco de dados -------------------------------------------
def existe_db():
    status = False

    try:
        db = conecta_db()
        cursor = db.cursor()

        cursor.execute("SHOW DATABASES")
        for banco in cursor:
            if banco == meu_db:
                status = True
        cursor.close()
        db.close()

    except BaseException as erro:
        print("Erro ao testar banco:" + str(erro))

    return status
#Criar um banco ----------------------------------------------------------------
def criar_db():

    try:
        db = conecta_db()
        cursor = db.cursor()

        cursor.execute("CREATE DATABASE " + meu_db[0])

        print("Banco de dados criado com susesso!")
        print("="*45)


        cursor.close()
        db.close()
        criar_tabela()


    except BaseException as erro:
        print("Falha ao criar banco de dados." + str(erro))


def criar_tabela():
    try:
        db = conecta_db(meu_db[0])
        cursor = db.cursor()

        sql = "CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, usuario VARCHAR(20), passwd VARCHAR(10))"
        cursor.execute(sql)

        sql = "CREATE TABLE livros (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), autor VARCHAR(255), editora VARCHAR(255), ano VARCHAR(4))"
        cursor.execute(sql)

        sql = "INSERT INTO usuarios (usuario, passwd) VALUES (%s, %s)"
        val = ("admin", "admin")
        cursor.execute(sql, val)


        db.commit()
        cursor.close()
        db.close()


    except  BaseException as erro:
        print("-"*45)
        print("Erro ao criar as tabelas." +str(erro))
        print("-"*45)


def valida_usroot():
    user = window.txt_usuario.text() #testei com window e nao foi tambem
    pswd = window.txt_senha.text() #tem um erro dizendo que self nao foi definido


    try:
        db = conecta_db(meu_db[0])
        cursor = db.cursor()

        cursor.execute("SELECT count(*) FROM usuarios")

        resultado = cursor.fetchone()
        teste = False


        tst1 = False
        tst2 = False

        if resultado[0] == 1:

            sql = "SELECT * FROM usuarios"
            cursor.execute(sql) #comando para executar
            usuarios = cursor.fetchone()

            if user == usuarios[1]:
                tst1 = True


            if pswd == usuarios[2]:
                tst2 = True



        if tst1 and tst2 == True:
            principal()
            window.close()
        else:
            class carrega_erro():
                janela = None
                def __init__(self):
                    global janela
                    self.jan = QtGui
                    self.arquivo = QFile('erro.ui')
                    self.arquivo.open(QFile.ReadOnly)
                    self.carrega = QUiLoader()
                    janela = self.carrega.load(self.arquivo)
                    self.arquivo.close()
                    janela.show()
            carrega_erro()


    except BaseException as erro:
        print("erro valida root"  + str(erro))
    finally:
        cursor.close()
        db.close()


#=====================class para carregar as janelas=========================================

class carrega_principal():
    janela = None
    def __init__(self):
        global janela
        self.jan = QtGui
        self.arquivo = QFile('jan_principal.ui')
        self.arquivo.open(QFile.ReadOnly)
        self.carrega = QUiLoader()
        janela = self.carrega.load(self.arquivo)



        janela.actionAdicionar_livro.triggered.connect(cad_livro)
        janela.actionAdicionar_alunos.triggered.connect(cadastro)
        janela.actionProcurar_livro.triggered.connect(pesquisar)
        janela.actionAjuda.triggered.connect(ajuda)

        #self.arquivo.close()
        janela.show()

class carregar_ajuda():
    janela = None
    def __init__(self):
        global janela
        self.jan = QtGui
        self.arquivo = QFile('ajuda.ui')
        self.arquivo.open(QFile.ReadOnly)
        self.carrega = QUiLoader()
        janela = self.carrega.load(self.arquivo)
        self.arquivo.close()
        janela.show()
        janela.btn_ok.clicked.connect(principal)

class carregar_cad_livro():
    janela = None
    def __init__(self):
        global janela
        self.jan = QtGui
        self.arquivo = QFile('cad_livro.ui')
        self.arquivo.open(QFile.ReadOnly)
        self.carrega = QUiLoader()
        janela = self.carrega.load(self.arquivo)
        self.arquivo.close()
        janela.show()
        janela.btn_voltar.clicked.connect(principal)
#====================função para cadastra livro======================================
        def cadastrar_livro():

            a = janela.txt_nome.text()
            b = janela.txt_autor.text()
            c = janela.txt_editora.text()
            d = janela.txt_ano.text()

            if len(a)>0 and len(b)>0 and len(c)>0 and len(d)>0:

                try:

                    db = conecta_db(meu_db[0])
                    cursor = db.cursor()


                    sql = "INSERT INTO livros(nome,autor,editora,ano) VALUES(%s, %s, %s, %s)"
                    val = (a, b, c, d)

                    cursor.execute(sql, val)

                    db.commit()
                    cursor.close()
                    db.close()
                    class cad_ok():
                        janela = None
                        def __init__(self):
                            global janela
                            self.jan = QtGui
                            self.arquivo = QFile('cad_ok.ui')
                            self.arquivo.open(QFile.ReadOnly)
                            self.carrega = QUiLoader()
                            janela = self.carrega.load(self.arquivo)
                            self.arquivo.close()
                            janela.show()
                            janela.btn_ok.clicked.connect(cad_livro)
                    cad_ok()


                except BaseException as erro:
                		print("Erro ao cadastrar livros.", str(erro))
            else:
                class cad_erro():
                    janela = None
                    def __init__(self):
                        global janela
                        self.jan = QtGui
                        self.arquivo = QFile('cad_erro.ui')
                        self.arquivo.open(QFile.ReadOnly)
                        self.carrega = QUiLoader()
                        janela = self.carrega.load(self.arquivo)
                        self.arquivo.close()
                        janela.show()
                        janela.btn_tentar.clicked.connect(cad_livro)
                cad_erro()


        janela.btn_cadsatrar.clicked.connect(cadastrar_livro)

#==============================================================================================
class carregar_novo_user():
    janela = None
    def __init__(self):
        global janela
        self.jan = QtGui
        self.arquivo = QFile('alterar_pswd.ui')
        self.arquivo.open(QFile.ReadOnly)
        self.carrega = QUiLoader()
        janela = self.carrega.load(self.arquivo)
        self.arquivo.close()
        janela.btn_voltar.clicked.connect(principal)
        janela.show()

#=============== função de alterar senha e usuario =====================================
        def alterar():
            a = janela.txt_novo_usuario.text()
            b = janela.txt_nova_senha.text()
            try:
                db = conecta_db(meu_db[0])
                cursor = db.cursor()
                sql = "SELECT * FROM usuarios"
                cursor.execute(sql, )
                resultado = cursor.fetchall()

                for r in resultado:
                    sql = "UPDATE usuarios SET usuario = %s, passwd = %s WHERE usuarios.id = " + str(r[0])
                    val = (a, b)
                    cursor.execute(sql, val)

                db.commit()
                cursor.close()
                db.close()

                class cad_ok():
                    janela = None
                    def __init__(self):
                        global janela
                        self.jan = QtGui
                        self.arquivo = QFile('altera_ok.ui')
                        self.arquivo.open(QFile.ReadOnly)
                        self.carrega = QUiLoader()
                        janela = self.carrega.load(self.arquivo)
                        self.arquivo.close()
                        janela.show()
                        janela.btn_ok.clicked.connect(principal)
                cad_ok()


            except BaseException as erro:

                print("Erro ao editar\n", str(erro))


        janela.btn_salvar.clicked.connect(alterar)
#==============================================================================================

class carregar_pesquisar():
    janela = None
    def __init__(self):
        global janela
        self.jan = QtGui
        self.arquivo = QFile('procurar.ui')
        self.arquivo.open(QFile.ReadOnly)
        self.carrega = QUiLoader()
        janela = self.carrega.load(self.arquivo)
        self.arquivo.close()
        janela.show()
        janela.btn_voltar.clicked.connect(principal)

#função para pesquisar
        def pesquisar_livros():
#=============== class para chamar janelas dentro dessa função ==============================
            class carrega_excluir():
                janela = None
                def __init__(self):
                    global janela
                    self.jan = QtGui
                    self.arquivo = QFile('excluir.ui')
                    self.arquivo.open(QFile.ReadOnly)
                    self.carrega = QUiLoader()
                    janela = self.carrega.load(self.arquivo)
                    self.arquivo.close()
                    janela.show()
                    janela.btn_canselar.clicked.connect(pesquisar)
                    janela.btn_ok.clicked.connect(delet)
                    janela.btn_ok.clicked.connect(pesquisar)

            class cad_ok():
                janela = None
                def __init__(self):
                    global janela
                    self.jan = QtGui
                    self.arquivo = QFile('altera_ok.ui')
                    self.arquivo.open(QFile.ReadOnly)
                    self.carrega = QUiLoader()
                    janela = self.carrega.load(self.arquivo)
                    self.arquivo.close()
                    janela.show()
                    janela.btn_ok.clicked.connect(pesquisar)


            class carrega_editar():
                janela = None
                def __init__(self):
                    global janela
                    self.jan = QtGui
                    self.arquivo = QFile('editar.ui')
                    self.arquivo.open(QFile.ReadOnly)
                    self.carrega = QUiLoader()
                    janela = self.carrega.load(self.arquivo)
                    self.arquivo.close()
                    janela.show()
                    janela.btn_salvar.clicked.connect(mudar)
                    janela.btn_salvar.clicked.connect(cad_ok)
                    janela.btn_voltar.clicked.connect(pesquisar)
#==============================================================================
            def excluir():
                j = carrega_excluir()
            n = janela.txt_nome.text()
            def editar():
                f = carrega_editar()

#===========================================================================
            try:
                db = conecta_db(meu_db[0])
                cursor = db.cursor()

                sql = "SELECT * FROM livros WHERE nome LIKE '%" + n + "%'"

                cursor.execute(sql)
                resultado = cursor.fetchall()

                for r in resultado:
                    janela.lbl_codigo.setText(str(r[0]))
                    janela.lbl_nome.setText(str(r[1]))
                    janela.lbl_autor.setText(str(r[2]))
                    janela.lbl_editora.setText(str(r[3]))
                    janela.lbl_ano.setText(str(r[4]))

                janela.btn_excluir.clicked.connect(excluir)
                janela.btn_editar.clicked.connect(editar)

#====================== função para deletar livros ==============================
                def delet():
                    db = conecta_db(meu_db[0])
                    cursor = db.cursor()

                    sql = "DELETE FROM livros WHERE livros.id = " + str(r[0])

                    cursor.execute(sql)
                    db.commit()
#===================== função para editar livros =================================
                def mudar():
                    db = conecta_db(meu_db[0])
                    cursor = db.cursor()

                    nome = janela.txt_nome2.text()
                    autor = janela.txt_autor.text()
                    editora = janela.txt_editora.text()
                    ano = janela.txt_ano.text()

                    if len(nome)>0 and len(autor)>0 and len(editora)>0 and len(ano)>0:
                        sql = "UPDATE livros SET nome = %s, autor = %s, editora = %s, ano = %s WHERE livros.id = " + str(r[0])
                        val = (nome, autor, editora, ano)

                        cursor.execute(sql, val)
                        db.commit()
                        cad_ok()

                    elif len(nome)>0 and len(autor)==0 and len(editora)==0 and len(ano)==0:
                        sql = "UPDATE livros SET nome = %s WHERE livros.id = " + str(r[0])
                        val = (nome, )

                        cursor.execute(sql, val)
                        db.commit()
                        cad_ok()

                    elif len(nome)==0 and len(autor)>0 and len(editora)==0 and len(ano)==0:
                        sql = "UPDATE livros SET autor = %s WHERE livros.id = " + str(r[0])
                        val = (autor, )

                        cursor.execute(sql, val)
                        db.commit()
                        cad_ok()

                    elif len(nome)==0 and len(autor)==0 and len(editora)>0 and len(ano)==0:
                        sql = "UPDATE livros SET editora = %s WHERE livros.id = " + str(r[0])
                        val = (editora, )

                        cursor.execute(sql, val)
                        db.commit()
                        cad_ok()

                    elif len(nome)==0 and len(autor)==0 and len(editora)==0 and len(ano)>0:
                        sql = "UPDATE livros SET ano = %s WHERE livros.id = " + str(r[0])
                        val = (ano, )
                        cursor.execute(sql, val)
                        db.commit()
                        cad_ok()


            except BaseException as erro:
                print("Erro ao pesquisar livros.", str (erro))

            finally:
                cursor.close()
                db.close()
        janela.btn_pesquisar.clicked.connect(pesquisar_livros)


        #janela.btn_ok.clicked.connect(delet)

#====================== Funções pra add as class em uma variável ====================
def ajuda():
    j = carregar_ajuda()
def pesquisar():
    a = carregar_pesquisar()

def cadastro():
    c = carregar_novo_user()

def principal():
    d = carrega_principal()
def cad_livro():
    e = carregar_cad_livro()



#Abertura da minha janela principal
if __name__ == "__main__":

	app = QApplication(sys.argv)#o sys vai capturar qualquer linha do seu sistema
	ui_file=QFile('login.ui')#trazer para dentro do código o arquivo .ui
	ui_file.open(QFile.ReadOnly)
	loader = QUiLoader()#carregar meu arquivo, gravar o arquivo dentro da variável window
	window = loader.load(ui_file)

	window.btn_entrar.clicked.connect(valida_usroot)

	ui_file.close()
	window.show() #pede para aparecer a janela

	if not existe_db():
		criar_db()
#precisa fazer entrar num loop, para o python não encerrer aqui e, cima
	sys.exit(app.exec_())
