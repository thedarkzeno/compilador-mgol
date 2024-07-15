from lexico import Token
import pandas as pd


class Parser:
    def __init__(self, action_table, goto_table, gramatica, scanner):
        self.action_table = action_table
        self.goto_table = goto_table
        self.gramatica = gramatica
        self.scanner = scanner
        self.stack = [0]
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
                token, use_hold_token = self.error_recovery(action, token, codigo)
                if use_hold_token == False:
                    self.hold_token = None
                continue
            elif action.startswith("s"):
                next_state = int("".join(action.split("s")[1:]))
                self.stack.append(token)
                self.stack.append(next_state)
                if self.hold_token != None:
                    token = self.hold_token
                    self.hold_token = None
                else:
                    token = self.scanner.scanner(codigo)
                print(f"Shift: {state} -> {next_state}")
            elif action.startswith("r"):
                production = self.gramatica["regra"][
                    int("".join(action.split("r")[1:]))
                ]
                lhs = production.split()[0].strip()
                rhs = production.split()[2:]

                for _ in range(len(rhs) * 2):
                    self.stack.pop()

                state = self.stack[-1]
                next_state = self.goto_table[
                    self.goto_table["goto"] == f"({state}, {lhs})"
                ]["estado"].to_list()[0]
                self.stack.append(lhs)
                self.stack.append(next_state)
                print(f"Reducing by: {lhs} -> {' '.join(rhs)}")
            elif action == "acc":
                print("Accepted")
                return
            else:
                self.hold_token = token
                token, use_hold_token = self.error_recovery(action, token, codigo)
                if use_hold_token == False:
                    self.hold_token = None
                continue

    def panic_mode(self, token: Token, codigo):
        print("Entrando em modo pânico...")
        candidateSymbols = []
        state = self.stack[-1]

        for k, v in self.action_table[self.action_table["estado"] == state].items():
            value = str(
                self.action_table[self.action_table["estado"] == state][k]
                .fillna("erro")
                .tolist()[0]
            )
            if "erro" not in value:
                candidateSymbols.append(k)

        print(f"Ignorando Token:", token)
        while token.classe not in candidateSymbols:
            token = self.scanner.scanner(codigo)
            if token.classe not in candidateSymbols:
                print(f"Ignorando Token:", token)
            if token.classe == "EOF":
                return Token(classe="$", lexema="EOF", tipo="Nulo")
        print(f"Recuperação com token de sincronização: {token.lexema}")
        return token

    def check_missing_tokens(self, token: Token, codigo):
        candidateSymbols = []
        state = self.stack[-1]

        for k, v in self.action_table[self.action_table["estado"] == state].items():
            value = str(
                self.action_table[self.action_table["estado"] == state][k]
                .fillna("erro")
                .tolist()[0]
            )
            if "erro" not in value:
                candidateSymbols.append(k)

        if "vir" in candidateSymbols:
            if token.classe == "id":
                print("Recuperação de erro", 'adicionando ","')
                return Token(classe="vir", lexema=",", tipo="Nulo")

        if "fc_p" in candidateSymbols:
            stack_contents = [
                item.lexema if hasattr(item, "classe") else item for item in self.stack
            ]
            open_parens = stack_contents.count("(")
            close_parens = stack_contents.count(")")
            if open_parens > close_parens:
                print("Recuperação de erro", 'adicionando ")"')
                return Token(classe="fc_p", lexema=")", tipo="Nulo")

        if "opm" in candidateSymbols:
            if token.classe == "id" or token.classe == "num":
                print("Recuperação de erro", 'adicionando "+"')
                return Token(classe="opm", lexema="+", tipo="Nulo")

        if "pt_v" in candidateSymbols:
            print("Recuperação de erro", 'adicionando ";"')
            token = Token(classe="pt_v", lexema=";", tipo="Nulo")

        if "inicio" in candidateSymbols:
            print("Recuperação de erro", 'adicionando "inicio"')
            token = Token("inicio", "inicio", "inicio")
            
        if "varinicio" in candidateSymbols:
            print("Recuperação de erro", 'adicionando "varinicio"')
            token = Token("varinicio", "varinicio", "varinicio")
            
        if "varfim" in candidateSymbols:
            print("Recuperação de erro", 'adicionando "varfim"')
            token = Token("varfim", "varfim", "varfim")

        if "fimse" in candidateSymbols:
            print("Recuperação de erro", 'adicionando "fimse"')
            token = Token("fimse", "fimse", "fimse")

        if "fim" in candidateSymbols:
            print("Recuperação de erro", 'adicionando "fim"')
            token = Token("fim", "fim", "fim")
        
        if "entao" in candidateSymbols:
            print("Recuperação de erro", 'adicionando "entao"')
            token = Token("entao", "entao", "entao")
        
        if "ab_p" in candidateSymbols:
            print("Recuperação de erro", 'adicionando "("')
            token = Token("ab_p", "(", "Nulo")

        return token

    def error_recovery(self, action, token: Token, codigo):
        lines = codigo.split("\n")
        print("____________________________\n")
        print("-------Erro Sintático-------")

        print(
            "** na linha:", self.scanner.linha, "e coluna:", self.scanner.coluna, "**"
        )

        print(lines[self.scanner.linha - 1])
        print(" " * max(0, int(self.scanner.coluna) - 2), "ˆ")
        print(" " * max(0, int(self.scanner.coluna) - 2), "|")

        print("____________________________\n")
        if action == "ERRO":
            print("Erro Léxico")
        prev_token = token
        use_hold_token = True
        token = self.check_missing_tokens(token, codigo)
        if token == prev_token:
            token = self.panic_mode(token, codigo)
            use_hold_token = False
        if token == prev_token:
            print("Não foi possível recuperar o erro!")
        print("____________________________\n")
        return token, use_hold_token
