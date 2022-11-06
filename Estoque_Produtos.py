from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser
import customtkinter
import sqlite3

janela = Tk()
p1 = PhotoImage(file='icone_caixa.png')
janela.iconphoto(False, p1)

class Relatorios():
    def printProduto(self):
        webbrowser.open("produtos.pdf")

    def geraRelatorioProduto(self):
        self.c = canvas.Canvas("produtos.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.produtoRel = self.nomeProduto.get()
        self.quantidadeRel = self.quantProduto.get()
        self.categoriaRel = self.categoriaProduto.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Produto')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Código: ')
        self.c.drawString(50, 670, 'Produto: ')
        self.c.drawString(50, 630, 'Quantidade: ')
        self.c.drawString(50, 600, 'Categoria: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(120, 700, self.codigoRel)
        self.c.drawString(140, 670, self.produtoRel)
        self.c.drawString(160, 630, self.quantidadeRel)
        self.c.drawString(160, 600, self.categoriaRel)

        self.c.rect(20, 720, 550, 200, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printProduto()

class Funcoes():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nomeProduto.delete(0, END)
        self.quantProduto.delete(0, END)
        self.categoriaProduto.delete(0, END)

    def conecta_bd(self):
        self.co = sqlite3.connect('produtos.bd')
        self.cursor = self.co.cursor();
        print('Conectando ao banco de dados')

    def desconecta_bd(self):
        self.co.close()

    def montaTabelas(self):
        self.conecta_bd()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos(
                cod INTEGER PRIMARY KEY, 
                nome_produto CHAR(40) NOT NULL, 
                quantidade INTEGER(20) NOT NULL, 
                categoria CHAR(30)
            ); 
        ''')

        self.co.commit();
        print('Banco de dados criado')
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nomeProduto.get()
        self.quantidade = self.quantProduto.get()
        self.categoria = self.categoriaProduto.get()

    def add_produto(self):
        self.variaveis()

        if self.nomeProduto.get() == '' and self.quantProduto.get() == '' and self.categoriaProduto.get() == '':
            msg = 'Os campos estão vazios!'
            messagebox.showinfo('Aviso!', msg)

        elif self.nomeProduto.get() == '':
            msg = 'Informar o NOME dos produtos!'
            messagebox.showinfo('Aviso!', msg)

        elif self.quantProduto.get() == '':
            msg = 'Informar a QUANTIDADE de produtos!'
            messagebox.showinfo('Aviso!', msg)

        elif self.categoriaProduto.get() == '':
            msg = 'Informar a CATEGORIA dos produtos!'
            messagebox.showinfo('Aviso!', msg)
        else:
            self.conecta_bd()
            self.cursor.execute(''' INSERT INTO produtos (nome_produto, quantidade, categoria)
                VALUES (?, ?, ?)''', (self.nome, self.quantidade, self.categoria))
            self.co.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(''' SELECT cod, nome_produto, quantidade, categoria FROM produtos
            ORDER BY nome_produto ASC; ''')

        for i in lista:
            self.listaCli.insert("", END, values=i)

        self.desconecta_bd()

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nomeProduto.insert(END, col2)
            self.quantProduto.insert(END, col3)
            self.categoriaProduto.insert(END, col4)

    def deleta_produto(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM produtos WHERE cod = ?""", (self.codigo,))
        self.co.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_produto(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" Update produtos SET nome_produto = ?, quantidade = ?, categoria = ? WHERE cod = ?""",
                            (self.nome, self.quantidade, self.categoria, self.codigo))
        self.co.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def busca_produto(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nomeProduto.insert(END, '%')
        nome = self.nomeProduto.get()
        self.cursor.execute(
            """SELECT cod , nome_produto, quantidade , categoria FROM produtos WHERE nome_produto LIKE '%s' ORDER BY nome_produto ASC""" % nome)
        buscanomeCLI = self.cursor.fetchall()
        for i in buscanomeCLI:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()

class Application(Funcoes, Relatorios):
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        janela.mainloop()

    def tela(self):
        self.janela.title('ESTOQUE DE PRODUTOS')
        self.janela.configure(background='#D75413')
        self.janela.geometry('788x588')
        self.janela.resizable(True, True)
        self.janela.minsize(width=788, height=588)

    def frames_tela(self):
        self.frame1 = Frame(self.janela, bd=4, bg='#dfe3ee', highlightbackground='#FF8C00', highlightthickness=3)
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame2 = Frame(self.janela, bd=4, bg='#dfe3ee', highlightbackground='#FF8C00', highlightthickness=3)
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.45)

    def widgets_frame1(self):
        # botão limpar...
        self.bt_limpar = customtkinter.CTkButton(self.frame1, text='Limpar', text_color='#ffffff', hover_color= 'grey', fg_color= '#D75413' ,text_font=('verdana', 8),
                                command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão buscar...
        self.bt_buscar = customtkinter.CTkButton(self.frame1, text='Buscar',text_color='#ffffff', hover_color= 'grey', fg_color= '#D75413' ,text_font=('verdana', 8), command = self.busca_produto)
        self.bt_buscar.place(relx=0.31, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão novo...
        self.bt_novo = customtkinter.CTkButton(self.frame1, text='Novo',text_color='#ffffff', hover_color= 'grey', fg_color= '#D75413' ,text_font=('verdana', 8),command=self.add_produto)
        self.bt_novo.place(relx=0.59, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão alterar...
        self.bt_alterar = customtkinter.CTkButton(self.frame1, text='Alterar',text_color='#ffffff', hover_color= 'grey', fg_color= '#D75413' ,text_font=('verdana', 8),command=self.altera_produto)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # botão apagar...
        self.bt_apagar = customtkinter.CTkButton(self.frame1, text='Apagar', text_color='#ffffff', hover_color= 'grey', fg_color= '#D75413' ,text_font=('verdana', 8),
                                command=self.deleta_produto)
        self.bt_apagar.place(relx=0.81, rely=0.1, relwidth=0.1, relheight=0.15)

        # criação label e entrada do codigo...
        self.label_codigo = Label(self.frame1, text='Código', bg='#dfe3ee', fg='#D75413')
        self.label_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.06)

        # criação label e entrada do nome do produto...
        self.label_nomeProduto = Label(self.frame1, text='Nome do Produto', bg='#dfe3ee', fg='#D75413')
        self.label_nomeProduto.place(relx=0.05, rely=0.35)

        self.nomeProduto = Entry(self.frame1)
        self.nomeProduto.place(relx=0.05, rely=0.45, relwidth=0.85)

        # criação label e entrada da quantidade de produtos...
        self.label_quantProduto = Label(self.frame1, text='Quantidade', bg='#dfe3ee', fg='#D75413')
        self.label_quantProduto.place(relx=0.05, rely=0.6)

        self.quantProduto = Entry(self.frame1)
        self.quantProduto.place(relx=0.05, rely=0.7, relwidth=0.4)

        # criação label e entrada da categoria do produto...
        self.label_categoriaProduto = Label(self.frame1, text='Categoria', bg='#dfe3ee', fg='#D75413')
        self.label_categoriaProduto.place(relx=0.5, rely=0.6)

        self.categoriaProduto = Entry(self.frame1)
        self.categoriaProduto.place(relx=0.5, rely=0.7, relwidth=0.4)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.column('#0', width=1, stretch=NO)
        self.listaCli.heading("#1", text='Código')
        self.listaCli.heading("#2", text='Nome do produto')
        self.listaCli.heading("#3", text='Quantidade')
        self.listaCli.heading("#4", text='Categoria')

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)
        style = ttk.Style(janela)
        style.theme_use('clam')

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame2, orient='vertical',
                                     command=self.listaCli.yview)
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu2 = Menu(menubar, tearoff=0)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatório", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu2.add_command(label="Ficha do produto", command=self.geraRelatorioProduto)

Application()