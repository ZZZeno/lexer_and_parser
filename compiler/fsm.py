from compiler.parser import *

class FSM:

    def __init__(self):
        self.state = []
        self.transfer = []   #dict
        self.goto = []

    def construct_DFA(self):   # construct DFA
        self.state = [closure(grammar, [grammar[0]])]
        self.transfer.append({})
        while 1:
            length = len(self.state)
            for index in range(0, len(self.state)):

                # print(len(item))
                for t in symbol + by_symbol:
                    goto_res = goto(self.state[index], t, grammar)

                    if len(goto_res) != 0:
                        flag = find_index(goto_res, self.state)
                        if flag == -1:
                            self.state.append(goto_res)
                            self.transfer.append({})
                            self.transfer[index][t] = len(self.state) - 1
                        else:
                            self.transfer[index][t] = flag

            if len(self.state) == length:
                return

    def output(self):   # format goto sentences output
        self.construct_DFA()
        cnt = 0
        res = []
        for x in self.state:
            tmp = str(cnt) + "\n"
            for y in x:
                tmp += str(y)
                tmp += "\n"
            tmp += "\n"
            cnt += 1
            res.append(tmp)

        for i in range(0, len(self.transfer)):
            for (k, v) in self.transfer[i].items():
                # print("goto({}, {}) = {}".format(i, k, v))
                res.append("goto({}, {}) = {}".format(i, k, v))
                self.goto.append((i, k, v))

        return res


def find_index(item, states):
    for i in range(0, len(states)):
        if set_is_equal(item, states[i]):
            return i
    return -1

def closure(g, p):   # construct production p's closure in grammar g
    productions = p
    while 1:
        length = len(productions)
        for item in productions:
            if item.dot_position == len(item.rhs):
                continue
            if item.rhs[item.dot_position] not in by_symbol:
                continue
            for p_in_g in g:
                if item.rhs[item.dot_position] == p_in_g.start_symbol and p_in_g.dot_position == 0:
                    if p_in_g not in productions:
                        productions.append(p_in_g)

        if len(productions) == length:
            break
    return productions



def goto(p, t, g):
    res = []
    for item in p:
        if item.dot_position < len(item.rhs) and item.rhs[item.dot_position] == t:
            res.append(production(item.start_symbol, item.rhs, item.dot_position+1))

    return closure(g, res)

def set_is_equal(p1, p2):   # check if set p1 and p2 are equal
    if len(p1) != len(p2):
        return False

    for item1 in p1:
        flag = False
        for item2 in p2:
            if prod_is_equal(item1, item2):
                flag = True
                break
        if flag == False:
            return False

    for item2 in p2:
        flag = False
        for item1 in p1:
            if prod_is_equal(item1, item2):
                flag = True
                break
        if flag == False:
            return False
    return True


def prod_is_equal(p1, p2):  #check production p1 and p2 are equal
    if (p1.start_symbol == p2.start_symbol
        and p1.rhs == p2.rhs
        and p1.dot_position == p2.dot_position):
        return True
    else:
        return False
