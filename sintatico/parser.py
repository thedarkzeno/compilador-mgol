from lexico import Token
import pandas as pd

class Parser:
    def __init__(self, action_table, goto_table, gramatica, scanner):
        self.action_table = action_table
        self.goto_table = goto_table
        self.gramatica = gramatica
        self.scanner = scanner
        self.stack = [0]
        self.sync_tokens = ["pt_v", "fc_p", "EOF"]
        self.hold_token = None


    def parse(self, codigo):
        token = self.scanner.scanner(codigo)  # (1) Primeiro símbolo de w$
        # print("token", token)
        while True:  # (2) Repita indefinidamente
            if token.classe == "EOF":
                token.classe = "$"
            if token.classe == "ERRO":
                # self.error_recovery("ERRO")
                return
            state = self.stack[-1]  # (3) Estado no topo da pilha
            action = self.action_table[token.classe][state]
            # print(token.lexema, token.classe, "state", state, "action", action)
            # print(token)
            # print(state)
            # print(action)
            if action is None or pd.isna(action):
                self.hold_token = token
                token = self.error_recovery(action, token, codigo)
                continue
            elif action.startswith('s'):  # (4) ACTION[s, a] = shift t
                next_state = int("".join(action.split("s")[1:]))
                self.stack.append(token)  # (5) Empilha t na pilha
                self.stack.append(next_state)
                if self.hold_token != None:
                    token = self.hold_token
                    self.hold_token = None
                else:
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
                self.hold_token = token
                token = self.error_recovery(action, token, codigo)  # (13) Recuperação de erro
                continue
    def panic_mode(self, token, codigo):
        while token.classe not in self.sync_tokens:
            token = self.scanner.scanner(codigo)
            print(token.lexema)
        return token
    
    def check_missing_tokens(self, token, codigo):
        stack_contents = [item.lexema if hasattr(item, 'classe') else item for item in self.stack]
        open_parens = stack_contents.count("(")
        close_parens = stack_contents.count(")")

        if open_parens > close_parens:
            print('Recuperação de erro', 'adicionando ")"')
            token = Token(classe="fc_p", lexema=")", tipo="Nulo")
        else:
            print('Recuperação de erro', 'adicionando ";"')
            token = Token(classe="pt_v", lexema=";", tipo="Nulo")
        
        return token



    def error_recovery(self, action, token, codigo):
        print("____________________________\n")
        print("-------Erro Sintático-------")

        print("** na linha:", self.scanner.linha, "e coluna:", self.scanner.coluna,"**")
        print(self.stack[-2])
        print("____________________________\n")
        if action == "ERRO":
            print("Erro Léxico")
        elif action == "erro_vir":
            print('Recuperação de erro', 'adicionando ","')
            return Token(classe="vir", lexema=",", tipo="Nulo")
        elif action == "erro_ptv" or action == "erro_exp" or action == "erro_fcp":
            return self.check_missing_tokens(token, codigo)
        else:
            return self.panic_mode(token, codigo)

