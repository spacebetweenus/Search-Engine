import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import search_engine
from bs4 import BeautifulSoup

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("1082x694+382+202")
        top.minsize(120, 1)
        top.maxsize(6038, 1586)
        top.resizable(1,  1)
        top.title("CS 121 PROJECT3")
        top.configure(background="#d9d9d9")

        self.top = top
        self.firstnum = 0
        self.lastnum = 0
        self.result = []
        self.dbpath = r'E:\UCI\2022 Winter\COMPSCI 121\P3\webpages\WEBPAGES_RAW\\'

        self.Entry1text = ''
        self.Entry1 = tk.Entry(self.top)
        self.Entry1.place(relx=0.266, rely=0.029, height=37, relwidth=0.494)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.793, rely=0.029, height=38, width=69)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=lambda : self.printnum(self.Entry1.get()))
        self.Button1.configure(compound='left')
        self.Button1.configure(cursor="fleur")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Search''')

        self.Text1 = tk.Text(self.top)
        self.Text1.place(relx=0.102, rely=0.115, relheight=0.735
                , relwidth=0.816)
        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="blue")
        self.Text1.configure(selectforeground="white")
        self.Text1.configure(wrap="word")

        self.Button2 = tk.Button(self.top)
        self.Button2.place(relx=0.545, rely=0.893, height=28, width=69)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(compound='left')
        self.Button2.configure(cursor="fleur")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Next''')
        self.Button2.configure(command=lambda : self.nextpage())

        self.Button3 = tk.Button(self.top)
        self.Button3.place(relx=0.397, rely=0.893, height=28, width=69)
        self.Button3.configure(activebackground="#ececec")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(compound='left')
        self.Button3.configure(cursor="fleur")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Previous''')
        self.Button3.configure(command=lambda : self.prevpage())


        self.Label1test = tk.StringVar()
        self.Label1 = tk.Label(self.top, textvariable = self.Label1test)
        self.Label1.place(relx=0.471, rely=0.893, height=23, width=72)
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(compound='left')
        self.Label1.configure(cursor="fleur")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1test.set('0/0')

    def printnum(self, s):
        self.Text1.delete(1.0, END)
        counter = 1.0
        self.result = search_engine.searchGUI(s)
        self.result = self.result.strip().split('\n')
        self.firstnum = 0
        self.lastnum = len(self.result)
        for i in self.result[self.firstnum:self.firstnum+10]:
            titlestr = ''
            with open(self.dbpath + (i.split(' (')[1][:-1]), 'r', encoding='UTF-8') as f:
                page = f.read()
                bs4page = BeautifulSoup(page, 'lxml')
                for title in bs4page.find_all('title'):
                    titlestr = title.get_text()
                    break
            self.Text1.insert(counter, i.split(' ')[0] + ' ' + titlestr  + '\n')
            counter += 1.0
            self.Text1.insert(counter, ' '.join(i.split(' ')[1:]).strip() + '\n')
            counter += 1.0
        # self.Label1test.set(int(self.Label1test.get().split('/')) )
        self.Label1test.set('0/' + str(self.lastnum))


    def prevpage(self):
        if self.firstnum == 0:
            return
        self.Text1.delete(1.0, END)
        counter = 1.0
        self.firstnum -= 10
        for i in self.result[self.firstnum:self.firstnum+10]:
            titlestr = ''
            with open(self.dbpath + (i.split(' (')[1][:-1]), 'r', encoding='UTF-8') as f:
                page = f.read()
                bs4page = BeautifulSoup(page, 'lxml')
                for title in bs4page.find_all('title'):
                    titlestr = title.get_text()
                    break
            self.Text1.insert(counter, i.split(' ')[0] + ' ' + titlestr  + '\n')
            counter += 1.0
            self.Text1.insert(counter, ' '.join(i.split(' ')[1:]).strip() + '\n')
            counter += 1.0
        self.Label1test.set(str(self.firstnum) + '/' + str(self.lastnum))

    def nextpage(self):
        if self.firstnum + 10 >= self.lastnum:
            return
        self.Text1.delete(1.0, END)
        counter = 1.0
        self.firstnum += 10
        for i in self.result[self.firstnum:self.firstnum+10]:
            titlestr = ''
            with open(self.dbpath + (i.split(' (')[1][:-1]), 'r', encoding='UTF-8') as f:
                page = f.read()
                bs4page = BeautifulSoup(page, 'lxml')
                for title in bs4page.find_all('title'):
                    titlestr = title.get_text()
                    break
            self.Text1.insert(counter, i.split(' ')[0] + ' ' + titlestr  + '\n')
            counter += 1.0
            self.Text1.insert(counter, ' '.join(i.split(' ')[1:]).strip() + '\n')
            counter += 1.0
        self.Label1test.set(str(self.firstnum) + '/' + str(self.lastnum))

if __name__ == '__main__':
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    _top1 = root
    _w1 = Toplevel1(_top1)
    root.mainloop()




