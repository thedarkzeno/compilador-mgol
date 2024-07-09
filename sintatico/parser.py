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
        token = self.scanner.scanner(codigo)  
        while True:
            if token.classe == "EOF":
                token.classe = "$"
            if token.classe == "ERRO":
                return
            state = self.stack[-1]  
            action = self.action_table[token.classe][state]

            if action is None or pd.isna(action):
                self.hold_token = token
                token = self.error_recovery(action, token, codigo)
                continue
            elif action.startswith('s'):  
                next_state = int("".join(action.split("s")[1:]))
                self.stack.append(token)  
                self.stack.append(next_state)
                if self.hold_token != None:
                    token = self.hold_token
                    self.hold_token = None
                else:
                    token = self.scanner.scanner(codigo)
                print(f"Shift: {state} -> {next_state}")
            elif action.startswith('r'):  
                production = self.gramatica["regra"][int("".join(action.split("r")[1:]))]
                lhs = production.split()[0].strip()
                rhs = production.split()[2:]
               
                for _ in range(len(rhs)*2):
                    self.stack.pop()
                
                state = self.stack[-1]
                next_state = self.goto_table[self.goto_table["goto"]==f"({state}, {lhs})"]["estado"].to_list()[0]
                self.stack.append(lhs)
                self.stack.append(next_state)
                print(f"Reducing by: {lhs} -> {' '.join(rhs)}")
            elif action == 'acc':
                print("Accepted")
                return
            else:
                self.hold_token = token
                token = self.error_recovery(action, token, codigo)
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

