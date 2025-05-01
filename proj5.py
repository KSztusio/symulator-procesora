import tkinter as tk
import rozkazy
root = tk.Tk()
root.geometry("920x600")
root.title("symulator procesora")
class bit:
    def __init__(self, posx, root):
        self.val = 0
        self.fr = tk.Frame(root, width = 7, height = 20, bg='white')
        self.fr.place(x=posx, y=2)
        self.label = tk.Label(root, text=self.val, width=1, height=1, bg='grey')
        self.label.place(x=posx-2, y=25)
    def update(self):
        self.label.config(text = str(self.val))
        if self.val == 1:
            self.fr.config(background = 'black')
        else:
            self.fr.config(background = 'white')
class bit8:
    def __init__(self, name, root, x):
        self.val = []
        self.name = name
        self.label = tk.Label(root, text=self.name, bg='grey')
        self.label.place(x=x+30, y = 45)
        for i in range(8):
            self.val.append(bit(x+9*i+2, root))
    def update(self):
        for b in self.val:
            b.update()
class rejestr:
    def __init__(self, name, x, y, root):
        self.frame = tk.Frame(root, width=150, height=70, bg='grey')
        self.frame.place(x = x, y = y)
        self.name = name
        self.label = tk.Label(root, text=self.name, width = 3)
        self.label.place(x=x+70, y=y-25)
        self.L = bit8(self.name[0]+'L', self.frame, 75)
        self.H = bit8(self.name[0]+'H', self.frame, 0)
    def update(self):
        self.L.update()
        self.H.update()
def rev(bin):
    tmp = ''
    for i in range(len(bin)):
        if bin[i] == '1':
            tmp += '0'
        else:
            tmp += '1'
    s = True
    k = 15
    while s:
        if tmp[k] == '0':
            tmp = tmp[0:k] + '1' + tmp[k+1:]
            s = False
        else:
            tmp = tmp[0:k] + '0' + tmp[k+1:]
        k-=1
    return tmp
def movrej(rej1, rej2):
    for i in range(8):
        rej1.L.val[i].val = rej2.L.val[i].val
        rej1.H.val[i].val = rej2.H.val[i].val
def movn(rej, number):
    for i in range(8):
        rej.L.val[i].val = int(number[8+i])
        rej.H.val[i].val = int(number[i])
def add(rej1, rej2, ax):
    tmp = ""
    b = 0
    for i in range(8):
        num = rej1.L.val[7-i].val + rej2.L.val[7-i].val + b
        if num > 1:
            num -= 2
            b = 1
        else:
            b = 0
        tmp = str(num) + tmp
    for i in range(8):
        num = rej1.H.val[7-i].val + rej2.H.val[7-i].val + b
        if num > 1:
            num -= 2
            b = 1
        else:
            b = 0
        tmp = str(num) + tmp
    for i in range(8):
        ax.H.val[i].val = int(tmp[i])
        ax.L.val[i].val = int(tmp[i+8])
def addn(rej, n, ax):
    tmp = ""
    b = 0
    for i in range(8):
        num = rej.L.val[7-i].val + int(n[15-i]) + b
        if num > 1:
            num -= 2
            b = 1
        else:
            b = 0
        tmp = str(num) + tmp
    for i in range(8):
        num = rej.H.val[7-i].val + int(n[7-i]) + b
        if num > 1:
            num -= 2
            b = 1
        else:
            b = 0
        tmp = str(num) + tmp
    for i in range(8):
        ax.H.val[i].val = int(tmp[i])
        ax.L.val[i].val = int(tmp[i+8])
def sub(rej1, rej2, ax):
    tmprej2 = ""
    for i in range(8):
        tmprej2 = tmprej2 + str(rej2.H.val[i].val)
    for i in range(8):
        tmprej2 = tmprej2 + str(rej2.L.val[i].val)
    tmprej2 = rev(tmprej2)
    addn(rej1, tmprej2, ax)
rejestry = [rejestr('AX', 10, 480, root),
            rejestr('BX', 170, 480, root),
            rejestr('CX', 330, 480, root),
            rejestr('DX', 490, 480, root)
             ]
rqueue = rozkazy.kol_rozkaz(root)
def read():
    rqueue.read()
    for rej in rejestry:
        rej.update()
    root.after(10, read)
    pass
def do_roz(rozkaz):
    if rozkaz[0].lower() == 'mov':
        if not rozkaz[2].isdigit() and not rozkaz[2][0] == '-':
            rej1 = rejestry[ord(rozkaz[1][0].upper())-65]
            rej2 = rejestry[ord(rozkaz[2][0].upper())-65]
            movrej(rej1, rej2)
        else:
            b = format(abs(int(rozkaz[2])), 'b')
            if len(b) < 16:
                b = '0' * (16-len(b)) + b
            if rozkaz[2][0] == '-':
                b = rev(b)
            rej = rejestry[ord(rozkaz[1][0].upper())-65]
            movn(rej, b)
    elif rozkaz[0].lower() == 'add' or rozkaz[0].lower() == 'sub':
        if not rozkaz[2].isdigit() and not rozkaz[2][0] == '-':
            rej1 = rejestry[ord(rozkaz[1][0].upper())-65]
            rej2 = rejestry[ord(rozkaz[2][0].upper())-65]
            if rozkaz[0].lower() == 'add':
                add(rej1, rej2, rejestry[0])
            else:
                sub(rej1, rej2, rejestry[0])
        else:
            rej = rejestry[ord(rozkaz[1][0].upper())-65]
            b = format(abs(int(rozkaz[2])), 'b')
            if len(b) < 16:
                b = '0' * (16-len(b)) + b
            if rozkaz[2][0] == '-':
                b = rev(b)
            if rozkaz[0].lower() == 'sub':
                b = rev(b)
            addn(rej, b, rejestry[0])
def program():
    rqueue.i = 0
    rqueue.krok = False
    if rqueue.is_ok():
        for rozkaz in rqueue.rozkaz:
            do_roz(rozkaz)
def krok():
    if rqueue.is_ok():
        rqueue.krok = True
        n = len(rqueue.rozkaz)
        if rqueue.i < n:
            rqueue.i += 1
            do_roz(rqueue.rozkaz[rqueue.i-1])
        else:
            rqueue.i = 0
            rqueue.krok = False
start = tk.Button(root, text = 'rozpocznij program', width = 17, height = 2, command = program)
prac_krok = tk.Button(root,text = 'praca krokowa', width = 17, height = 2, command = krok)
prac_krok.place(x = 780, y = 500)
start.place(x = 650, y = 500)
save = tk.Button(root, text = 'save code',  width = 17, height = 2, command = rqueue.save)
load = tk.Button(root, text = 'load code',  width = 17, height = 2, command = rqueue.load)
save.place(x = 650, y = 550)
load.place(x = 780, y = 550)
root.after(10, read)
root.mainloop()