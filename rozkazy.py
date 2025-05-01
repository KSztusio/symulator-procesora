import tkinter as tk
from tkinter import filedialog as fd
class kol_rozkaz:
    i = 0
    krok = False
    rozkaz = []
    q = []
    tagname = []
    def __init__(self, root):
        self.tx = tk.Text(root, width = 30, height = 30)
        self.tx.place(x = 650, y = 10)
    def check(self, line, i):
        error = False
        line = line.lower()
        if (line[0:3] == 'mov' or line[0:3] == 'sub' or line[0:3] == 'add') and len(line) > 3:
            if line[3] == ' ' and len(line) > 5:
                if (line[4:6] == 'ax' or line[4:6] == 'bx' or line[4:6] == 'cx' or line[4:6] == 'dx') and len(line) > 6:
                    if line[6] == ',' and len(line) > 7:
                        if line[7] == ' ' and len(line) > 8:
                            if line[8].isdigit():
                                if not line[8:].isdigit():
                                    error = True
                            elif line[8] == '-':
                                if not line[9:].isdigit():
                                    error = True
                            elif line[8] in "abcd" and len(line) == 10:
                                if line[9] == 'x':
                                    pass
                                else:
                                    error = True
                            else:
                                error = True
                        else:
                            error = True
                    else:
                        error = True
                else:
                    error = True
            else:
                error = True
        else:
            error = True
        if len(line) == 0:
            error = False
        if error:
            self.i = 0
            self.krok = False
            st = str(i+1) + '.' + '0'
            end = str(i+1) + '.' + 'end'
            self.tagname.append(str(i+1))
            self.tx.tag_add(str(i+1), st, end)
            self.tx.tag_config(str(i+1), background='red')
    def read(self):
        self.q = self.tx.get("1.0", "end-1c").split('\n')
        self.tx.tag_delete("active")

        for tag in self.tagname:
            self.tx.tag_delete(tag)
        if self.krok:
            self.tx.tag_add("active", str(self.i)+".0", str(self.i)+".end")
            self.tx.tag_config("active", background = "yellow")
        self.tagname = []
        for i in range(len(self.q)):
            self.check(self.q[i], i)
        self.rozkaz = []
        for r in self.q:
            self.rozkaz.append([r[0:3], r[4:6], r[8:]])
    def is_ok(self):
        if self.tagname == []:
            return True
        else:
            return False
    def save(self):
        if self.is_ok():
            filename = fd.asksaveasfile(mode='w')
            with open(filename.name, 'w') as file:
                for i in range (len(self.q)):
                    file.write(self.q[i] + '\n' * (i < len(self.q)))
    def load(self):
        filename = fd.askopenfile(mode='r')
        with open(filename.name, 'r') as file:
            self.q = file.readlines()
            print(self.q)
            self.tx.delete("1.0", "end-1c")
            for i in range (len(self.q)):
                self.tx.insert(str(i+1)+".0", self.q[i])