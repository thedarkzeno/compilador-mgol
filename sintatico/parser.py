class Parser:
    def __init__(self, action_table, goto_table, gramatica, scanner):
        self.action_table = action_table
        self.goto_table = goto_table
        self.gramatica = gramatica
        self.scanner = scanner
        self.stack = [0]




    def parse(self, codigo):
        token = self.scanner.scanner(codigo)  # (1) Primeiro símbolo de w$
        print("token", token)
        while True:  # (2) Repita indefinidamente
            if token.classe == "EOF":
                token.classe = "$"
            state = self.stack[-1]  # (3) Estado no topo da pilha
            action = self.action_table[token.classe][state]
            print(token)
            print(state)
            if action is None:
                self.error_recovery()
                return
            elif action.startswith('s'):  # (4) ACTION[s, a] = shift t
                next_state = int("".join(action.split("s")[1:]))
                self.stack.append(token)  # (5) Empilha t na pilha
                self.stack.append(next_state)
                token = self.scanner.scanner(codigo)  # (6) Próximo símbolo da entrada
            elif action.startswith('r'):  # (7) ACTION[s, a] = reduce A -> β
                production = self.gramatica["regra"][int("".join(action.split("r")[1:]))]
                lhs = production.split()[0].strip()
                rhs = production.split()[2:]#.strip().split()
                # print("token", token)
                for _ in range(len(rhs)*2):  # (8) Desempilha símbolos |β| da pilha
                    self.stack.pop()
                
                state = self.stack[-1]  # (9) Estado t no topo da pilha
                next_state = self.goto_table[self.goto_table["goto"]==f"({state}, {lhs})"]["estado"].to_list()[0]
                self.stack.append(lhs)
                self.stack.append(next_state)  # (10) Empilha GOTO[t, A] na pilha
                print(f"Reducing by: {lhs} -> {' '.join(rhs)}")  # (11) Imprime a produção A -> β
            elif action == 'acc':  # (12) ACTION[s, a] = accept
                print("Accepted")
                return
            else:
                self.error_recovery()  # (13) Recuperação de erro
                return

    def error_recovery(self):
        print("Syntax error")
