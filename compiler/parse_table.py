from compiler.fsm import *
from prettytable import PrettyTable


# demo action ('s', 3)

class Parse_table:
    def __init__(self):
        self.action_table = []   # a list of dict  [ {key: ('s', 3)}, {} ]
        self.goto_table = []     # a list of dict [ {key: 3} ]

        self.first = []
        self.follow = {}
        self.parse_steps = []
        self.action_goto_table = []

    def fill_goto_table(self):
        test = FSM()
        test.construct_DFA()
        for i in range(0, len(test.state)):
            self.goto_table.append({})
            self.action_table.append({})

        test.output()
        for x in test.goto:
            if x[1] in by_symbol:
                self.goto_table[x[0]][x[1]] = x[2]
            else:
                self.action_table[x[0]][x[1]] = ('s', x[2])
        self.follow_set("S'")  # Start symbol is S', construct follow set
        first_row = ['States'] + symbol + by_symbol
        self.action_goto_table = PrettyTable(first_row)
        for i in range(0, len(test.state)):
            add_list = []
            for j in range(0, len(first_row)):
                add_list.append("")
            add_list[0] = str(i)
            for k, v in self.goto_table[i].items():
                add_list[eval(k)+1] = self.goto_table[i][k]

            for x in test.state[i]:
                if x.dot_position == len(x.rhs):
                    for k, vs in self.follow.items():
                        for g_i in range(0, len(grammar)):
                            if x.start_symbol == k \
                                    and x.rhs == grammar[g_i].rhs\
                                    and x.start_symbol == grammar[g_i].start_symbol:
                                for v in vs:
                                    if v == "$":
                                        v = "EOF"
                                    if g_i == 0:
                                        add_list[eval(v)+1] = "accept"
                                        self.action_table[i][v] = "accept"
                                        continue
                                    if v not in self.action_table[i].keys():
                                        self.action_table[i][v] = ('r', g_i)
                                    add_list[eval(v)+1] = "r" + str(g_i)

            for k, v in self.action_table[i].items():
                add_list[eval(k)+1] = str(self.action_table[i][k][0])+str(self.action_table[i][k][1])
            self.action_goto_table.add_row(add_list)

    def first_set(self, s):
        ret = []
        if s in symbol:
            return [s]
        while 1:
            length = len(ret)
            for g in grammar:
                if g.start_symbol != s:
                    continue
                if len(g.rhs) == 0 and "" not in ret:
                    ret.append("")
                for r in g.rhs:
                    if r == s:
                        if "" not in ret:
                            break
                        else:
                            continue
                    rhs_first = self.first_set(r)
                    for x in rhs_first:
                        if x not in ret:
                            ret.append(x)
                    if "" not in rhs_first:
                        break
            if length == len(ret):
                break
        return ret

    def first_s_set(self, t):
        ret = []
        if len(t) == 0:
            return ret
        ret += self.first_set(t[0])
        i = 0
        while i < len(t)-1 and "" in self.first_set(t[i]):
            for x in self.first_set(t[i+1]):
                if x not in ret:
                    ret.append(x)
            i += 1
        return ret

    def follow_set(self, s):
        follow = {}
        for x in by_symbol:
            follow[x] = []
        follow["S'"] = ['$']
        while 1:
            length = self.items_in_dict(follow)
            for sym in by_symbol:
                for g in grammar:
                    cnt = self.count(sym, g)
                    if len(cnt) == 0:
                        continue
                    for i in cnt:
                        if i < len(g.rhs) - 1:
                            for x in self.first_s_set(g.rhs[i+1:]):
                                if x != "" and x not in follow[sym]:
                                    follow[sym].append(x)
                            if "" in self.first_s_set(g.rhs[i+1:]):
                                for x in follow[g.start_symbol]:
                                    if x not in follow[sym]:
                                        follow[sym].append(x)
                        if i == len(g.rhs) - 1:
                            for x in follow[g.start_symbol]:
                                if x not in follow[sym]:
                                    follow[sym].append(x)
            if length == self.items_in_dict(follow):
                break
        self.follow = follow

    def items_in_dict(self, dict):
        length = 0
        for key in dict:
            length += len(dict[key])
        return length

    def count(self, s, p):
        ret = []
        for i in range(0, len(p.rhs)):
            if p.rhs[i] == s:
                ret.append(i)
        return ret

    def analysis(self, items_list):   # analyse the token
        items_list.append(('EOF', None, items_list[-1][2] + 1))
        accept_list = []
        states_list = []
        states_list.append(0)
        i = 0
        j = 0
        while 1:
            j += 1
            next_action = self.action_table[states_list[-1]][items_list[i][0]]
            if next_action[0] == "s":
                accept_list.append(items_list[i][0])
                states_list.append(next_action[1])
                i += 1
            elif next_action[0] == "r":
                cnt = len(grammar[next_action[1]].rhs)
                for p in range(0, cnt):
                    accept_list.pop()
                    states_list.pop()
                accept_list.append(grammar[next_action[1]].start_symbol)
                states_list.append(self.goto_table[states_list[-1]][accept_list[-1]])

            step = []
            for x in accept_list:
                step.append(x)
            self.parse_steps.append(step)
            if states_list[-1] == 3:
                break

    def run(self, token_list):
        self.fill_goto_table()
        self.analysis(token_list)
