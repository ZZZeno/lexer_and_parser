from compiler.token import *


class Rules:
    def __init__(self, sources: str):
        self.sources = sources
        self.current_line = 1
        self.items = []
        self.symbol_table = []

    def parse_FLOAT_TYPE(self):
        self.line_counter()

        if (len(self.sources) >= 5
            and self.sources[0:5] == "float"
            and self.sources[5] in " \n\t"):
            self.items.append((symbol[FLOAT_TYPE], None, self.current_line))
            self.sources = self.sources[5:]

    def parse_INT_TYPE(self):
        self.line_counter()
        if (len(self.sources) >= 3
            and self.sources[0:3] == "int"
            and self.sources[3] in " \t\n"):
            self.items.append((symbol[INT_TYPE], None, self.current_line))
            self.sources = self.sources[3:]

    def parse_FLOAT_CONST(self):
        self.line_counter()
        cur_pos = 0
        cur_state = 0
        while 1:
            if cur_state == 0:
                if cur_pos == len(self.sources):
                    break
                if self.sources[cur_pos].isdigit():
                    cur_state = 1
                    cur_pos += 1
                    continue
                elif self.sources[cur_pos] == ".":
                    cur_state = 3
                    cur_pos += 1
                    continue
                else:
                    break
            if cur_state == 1:
                if cur_pos == len(self.sources):
                    cur_pos = 0
                    break
                if self.sources[cur_pos].isdigit():
                    cur_pos += 1
                elif self.sources[cur_pos] == ".":
                    cur_state = 2
                    cur_pos += 1
                    continue
                else:
                    cur_pos = 0
                    break
            if cur_state == 2:
                if cur_pos == len(self.sources):
                    break
                if self.sources[cur_pos].isdigit():
                    cur_pos += 1
                    continue
                else:
                    break
            if cur_state == 3:
                if cur_pos == len(self.sources):
                    cur_pos = 0
                    break
                if self.sources[cur_pos].isdigit():
                    cur_pos += 1
                    cur_state = 4
                    continue
                else:
                    cur_pos = 0
                    break
            if cur_state == 4:
                if cur_pos == len(self.sources):
                    break
                if self.sources[cur_pos].isdigit():
                    cur_pos += 1
                else:
                    break

        if cur_pos != len(self.sources):
            if self.sources[cur_pos].isalpha() or self.sources[cur_pos] == "_":
                cur_pos = 0
                
        if cur_pos != 0:
            self.items.append((symbol[FLOAT_CONST], self.sources[0:cur_pos], self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_INT_CONST(self):
        self.line_counter()
        cur_pos = 0
        while cur_pos < len(self.sources) and self.sources[cur_pos].isdigit():
            cur_pos += 1

        if cur_pos != len(self.sources):
            if self.sources[cur_pos].isalpha() or self.sources[cur_pos] == "_":
                cur_pos = 0
                
        if cur_pos != 0:
            self.items.append((symbol[INT_CONST], self.sources[0:cur_pos], self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_ID(self):
        self.line_counter()
        cur_pos = 0
        cur_state = 0
        while 1:
            if cur_state == 0:
                if cur_pos == len(self.sources):
                    break
                if self.sources[cur_pos].isalpha() or self.sources[cur_pos] == "_":
                    cur_pos += 1
                    cur_state = 1
                    continue
                else:
                    cur_pos = 0
                    break
            if cur_state == 1:
                if cur_pos == len(self.sources):
                    break
                if (self.sources[cur_pos].isalpha()
                    or self.sources[cur_pos].isdigit()
                    or self.sources[cur_pos] == "_"):
                    cur_pos += 1
                else:
                    break
        if cur_pos != 0:
            tmp_id = self.sources[0:cur_pos]
            if tmp_id not in self.symbol_table:
                self.symbol_table.append(tmp_id)
            for i in range(0, len(self.symbol_table)):
                if tmp_id == self.symbol_table[i]:
                    self.items.append((symbol[ID], i, self.current_line))


        self.sources = self.sources[cur_pos:]

    def parse_LEFT_PARENTHESIS(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == "(":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[LEFT_PARENTHESIS], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_RIGHT_PARENTHESIS(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == ")":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[RIGHT_PARENTHESIS], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_ADD(self):
         self.line_counter()
         cur_pos = 0
         if cur_pos == len(self.sources):
             return
         if self.sources[cur_pos] == "+":
             cur_pos += 1
         if cur_pos != 0:
            self.items.append((symbol[ADD_OP], None, self.current_line))
         self.sources = self.sources[cur_pos:]

    def parse_SUB(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == "-":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[SUB_OP], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_MULTI(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == "*":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[MUL_OP], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_DIV(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == "/":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[DIV_OP], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_EQ(self):
        self.line_counter()
        cur_pos = 0
        if len(self.sources) >= 2 and self.sources[0:2] == "==":
            cur_pos += 2
        if cur_pos != 0:
            self.items.append((symbol[IS_EQ_OP], None, self.current_line))
        self.sources = self.sources[cur_pos:]
        

    def parse_LT(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == "<":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[LT_OP], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_GT(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == ">":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[GT_OP], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_SEMICOLON(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == ";":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[SEMI], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_ASSIGN(self):
        self.line_counter()
        cur_pos = 0
        if cur_pos == len(self.sources):
            return
        if self.sources[cur_pos] == "=":
            cur_pos += 1
        if cur_pos != 0:
            self.items.append((symbol[ASSIGN], None, self.current_line))
        self.sources = self.sources[cur_pos:]

    def parse_WHILE(self):
        self.line_counter()

        if (len(self.sources) >= 5
            and self.sources[0:5] == "while"
            and self.sources[5] in " \n\t"):

            self.items.append((symbol[WHILE_KEYWORD], None, self.current_line))
            self.sources = self.sources[5:]

    def parse_IF(self):
        self.line_counter()

        if (len(self.sources) >= 2
            and self.sources[0:2] == "if"
            and self.sources[2] in " \n\t"):
            self.items.append((symbol[IF_KEYWORD], None, self.current_line))
            self.sources = self.sources[2:]

    def parse_ELSE(self):
        self.line_counter()

        if (len(self.sources) >= 4
            and self.sources[0:4] == "else"
            and self.sources[4] in " \n\t"):
            self.items.append((symbol[ELSE_KEYWORD], None, self.current_line))
            self.sources = self.sources[4:]

    def line_counter(self): 
        while 1:
            if self.sources == "":
                return
            if self.sources[0] == " " or self.sources[0] == "\t":
                self.sources = self.sources[1:]
            elif self.sources[0] == "\n":
                self.current_line += 1
                self.sources = self.sources[1:]
            else:
                return
            
    def run(self):
        while self.sources != "":
            self.parse_FLOAT_TYPE()
            self.parse_INT_TYPE()
            self.parse_FLOAT_CONST()
            self.parse_INT_CONST()
            self.parse_WHILE()
            self.parse_IF()
            self.parse_ELSE()
            self.parse_ID()
            self.parse_LEFT_PARENTHESIS()
            self.parse_RIGHT_PARENTHESIS()
            self.parse_ADD()
            self.parse_SUB()
            self.parse_MULTI()
            self.parse_DIV()
            self.parse_EQ()
            self.parse_ASSIGN()
            self.parse_LT()
            self.parse_GT()
            self.parse_SEMICOLON()
