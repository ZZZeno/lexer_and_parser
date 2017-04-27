from compiler.token import *

class production:

    def __init__(self, start_symbol, rhs, dot_position):
        self.start_symbol = start_symbol
        self.rhs = rhs     # a list
        self.dot_position = dot_position

    def __str__(self):  # format grammar
        res = ""
        res += self.start_symbol
        res += " ->"
        cnt = 0
        for x in self.rhs:
            if cnt == self.dot_position:
                res += " ."
            res += " " + x
            cnt += 1
        if self.dot_position == len(self.rhs):
            res += " ."
        return res


grammar =[    # grammar
    production("S'", ['P'], 0),
    production('P', ['D', 'S'], 0),
    production('D', ['L', 'ID', 'SEMI', 'D'], 0),
    production('D', [], 0),
    production('L', ['INT_TYPE'], 0),
    production('L', ['FLOAT_TYPE'], 0),
    production('S', ['ID', 'ASSIGN', 'E'], 0),
    production('S', ['IF_KEYWORD', 'LEFT_PARENTHESIS', 'C', 'RIGHT_PARENTHESIS', 'S'], 0),
    production('S', ['IF_KEYWORD', 'LEFT_PARENTHESIS', 'C', 'RIGHT_PARENTHESIS', 'S', 'ELSE_KEYWORD', 'S'], 0),
    production('S', ['WHILE_KEYWORD', 'LEFT_PARENTHESIS', 'C', 'RIGHT_PARENTHESIS', 'S'], 0),
    production('S', ['S', 'SEMI', 'S'], 0),
    production('S', [], 0),
    production('C', ['E', 'GT_OP', 'E'], 0),
    production('C', ['E', 'LT_OP', 'E'], 0),
    production('C', ['E', 'IS_EQ_OP', 'E'], 0),
    production('E', ['E', 'ADD_OP', 'T'], 0),
    production('E', ['E', 'SUB_OP', 'T'], 0),
    production('E', ['T'], 0),
    production('T', ['F'], 0),
    production('T', ['T', 'MUL_OP', 'F'], 0),
    production('T', ['T', 'DIV_OP', 'F'], 0),
    production('F', ['LEFT_PARENTHESIS', 'E', 'RIGHT_PARENTHESIS'], 0),
    production('F', ['ID'], 0),
    production('F', ['INT_CONST'], 0),
]
