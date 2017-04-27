INT_CONST = 0
FLOAT_CONST = 1
INT_TYPE = 2
FLOAT_TYPE = 3
ID = 4

LEFT_PARENTHESIS = 5
RIGHT_PARENTHESIS = 6

ADD_OP = 10
SUB_OP = 9
MUL_OP = 8
DIV_OP = 7

IS_EQ_OP = 11
LT_OP = 12
GT_OP = 13

SEMI = 14
WHILE_KEYWORD = 15
IF_KEYWORD = 16
ELSE_KEYWORD = 17
ASSIGN = 18
EOF = 19

symbol = [     # terminal symbol list
    "INT_CONST",
    "FLOAT_CONST",
    "INT_TYPE",
    "FLOAT_TYPE",
    "ID",
    "LEFT_PARENTHESIS",
    "RIGHT_PARENTHESIS",
    "DIV_OP",
    "MUL_OP",
    "SUB_OP",
    "ADD_OP",
    "IS_EQ_OP",
    "LT_OP",
    "GT_OP",
    "SEMI",
    "WHILE_KEYWORD",
    "IF_KEYWORD",
    "ELSE_KEYWORD",
    "ASSIGN",
    "EOF",
]

by_symbol = [   # non terminal symbols in grammar
    "S'",
    "P",
    "D",
    "S",
    "L",
    "E",
    "C",
    "T",
    "F"
]

SDASH = 20
P = 21
D = 22
S = 23
L = 24
E = 25
C = 26
T = 27
F = 28