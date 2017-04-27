import tkinter as tk
from compiler.rules import *
from compiler.fsm import *
from compiler.parse_table import *


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.src = ""
        self.token_list = []

    def create_widgets(self):
        self.text_editor = tk.Entry(self, width=50)
        self.text_editor.bind('<Return>', self.set_text)
        self.text_editor.pack(side="top")
        self.result = tk.Label(self)
        self.result.pack()
        self.test_text = tk.Text(self)
        self.test_text.pack()
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")
        
    def get_text(self):
        self.src = self.text_editor.get()

    def set_text(self, event):
        self.get_text()
        lexer = Rules(self.src)
        lexer.run()
        self.test_text.insert('end', "The action & goto table has been written to the file action_n_goto_table.txt\n", 'alert')
        self.test_text.tag_configure('alert', background='green', foreground='black')
        self.test_text.insert('end', '\n')

        self.test_text.insert('end', "Grammar\n", 'grammar')
        self.test_text.tag_configure('grammar', background='black', foreground='green')

        # output the grammmar
        g = ""
        for x in grammar:
            g += x.start_symbol
            g += " ->"
            for y in x.rhs:
                g += " "
                g += y
            g += '\n'
        g += '\n'

        self.test_text.insert('end', g)

        #output tokens
        self.test_text.insert('end', "Token\n", 'token')
        self.test_text.tag_configure('token', background='black',  foreground='green')

        for x in lexer.items:
            self.test_text.insert('end', x[0])
            self.test_text.insert('end', ' ')
            self.token_list.append(x)
        for x in range(0, 3):
            self.test_text.insert('end', '\n')

        #output states
        self.test_text.insert('end', "States:\n", 'states')
        self.test_text.tag_configure('states', foreground='green', background='black')

        fsm = FSM()
        fsm_res = fsm.output()

        #output goto sentences
        goto_flag = False
        for x in fsm_res:
            if not x[0].isdigit():
                if goto_flag == False:
                    self.test_text.insert('end', 'Goto Sentences:\n', 'goto')
                    self.test_text.tag_configure('goto', foreground='green', background='black')
                goto_flag = True
            self.test_text.insert('end', x)
            self.test_text.insert('end', '\n')
        self.test_text.insert('end', '\n')

        #output parse stack
        self.test_text.insert('end', "Parse Stack:\n", 'parse_stack')
        self.test_text.tag_configure('parse_stack', foreground='green', background='black')
        parse_table = Parse_table()
        parse_table.run(self.token_list)
        for x in parse_table.parse_steps:
            for y in x:
                self.test_text.insert('end', y + "  ")
            self.test_text.insert('end', '\n')
        f = open('action_n_goto_table.txt', 'w')
        f.write(str(parse_table.action_goto_table))
        f.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()