from lexico import Token

def traduz_tipo(tipo):
    if tipo == "inteiro":
        return "int"
    if tipo == "real":
        return "double"
    if tipo == "literal":
        return "literal"


class SemanticAnalyzer:
    def __init__(self, scanner):
        self.scanner = scanner
        self.symbol_table = {}
        self.filename = "PROGRAMA.c"
        self.code = []
        self.error = False
        self.current_type = None
        self.arg = None
        self.hold_temp_line = ""

        self.pilha_semantica = []
        self.temp_count=0
    
    def handle_error(self, msg=None):
        self.error = True
        lines = self.codigo.split("\n")
        print("____________________________\n")
        print("-------Erro Semântico-------")
        if msg:
            print(msg, "\n")
        print(lines[self.scanner.linha - 1])
        print(" " * max(0, int(self.scanner.coluna) - 2), "ˆ")
        print(" " * max(0, int(self.scanner.coluna) - 2), "|")
        print(
            "** na linha:", self.scanner.linha, "e coluna:", self.scanner.coluna, "**"
        )
        
        print("____________________________\n")
        pass
    
    def get_id(self, pilha_sintatica):
        pilha = list(reversed(pilha_sintatica))
        for el in pilha:
            if isinstance(el, Token) and el.classe == "id":
                token = self.symbol_table.get(el.lexema, Token("id", el.lexema, "Nulo"))
                if token.tipo == "Nulo":
                    self.handle_error(msg="Variável não declarada")
                    return token, True
                return token, False
        return None, True
    
    def add_blank_lines(self):
        self.code.append("\n\n\n")

    def update_symbol_table(self):
        if self.current_type:
            for key in self.symbol_table:
                if self.symbol_table[key].tipo == "Nulo":
                    self.symbol_table[key].tipo = self.current_type

    def add_ids_to_symbol_table(self, pilha_sintatica):
        for el in pilha_sintatica:
            if isinstance(el, Token) and el.classe == "id":
                token = self.symbol_table.get(el.lexema, Token("id", el.lexema, "Nulo"))
                self.symbol_table[el.lexema] = token

    def add_id_to_symbol_table(self, pilha_sintatica):
        id_token = pilha_sintatica[-2]
        token = self.symbol_table.get(id_token.lexema, Token("id", id_token.lexema, "Nulo"))
        self.symbol_table[id_token.lexema] = token

    def save_current_type(self, pilha_sintatica):
        token = pilha_sintatica[-2]
        self.current_type = token.lexema

    def handle_leia(self, pilha_sintatica):
        token, erro = self.get_id(pilha_sintatica)
        if not erro:
            if token.tipo == "literal":
                self.code.append(f'scanf("%s", {token.lexema});\n')
            elif token.tipo == "inteiro":
                self.code.append(f'scanf("%d", &{token.lexema});\n')
            elif token.tipo == "real":
                self.code.append(f'scanf("%lf", &{token.lexema});\n')

    def handle_escreva(self):
        token = self.pilha_semantica[-1]
        lexema = token.lexema.replace('"', '')
        if token.tipo == "lit":
            self.code.append(f'printf("{lexema}");\n')
        elif token.tipo == "literal":
            self.code.append(f'printf("%s", {lexema});\n')
        elif token.tipo == "inteiro":
            self.code.append(f'printf("%d", {lexema});\n')
        elif token.tipo == "real":
            self.code.append(f'printf("%lf", {lexema});\n')

    def add_to_pilha_semantica(self, pilha_sintatica):
        token = pilha_sintatica[-2]
        self.pilha_semantica.append(token)

    def handle_assign(self, pilha_sintatica):
        temp = self.pilha_semantica[-1]
        token, erro = self.get_id(pilha_sintatica)
        if not erro and temp.tipo == token.tipo:
            self.code.append(f"{token.lexema} = {temp.lexema};\n")
        else:
            self.handle_error(f"Tipo de {temp.lexema} != Tipo de {token.lexema}")

    def handle_ld(self, pilha_sintatica):
        for el in pilha_sintatica:
            if isinstance(el, Token):
                opm = el
        if (self.pilha_semantica[-1].tipo == self.pilha_semantica[-2].tipo and 
            self.pilha_semantica[-1].tipo != "literal"):
            tipo = self.pilha_semantica[-1].tipo
            opm1 = self.pilha_semantica[-1]
            opm2 = self.pilha_semantica[-2]
            self.temp_count += 1
            self.pilha_semantica = self.pilha_semantica[:-2]
            self.pilha_semantica.append(Token("temp", f"T{self.temp_count}", tipo))
            self.code.append(f"T{self.temp_count} = {opm2.lexema} {opm.lexema} {opm1.lexema};\n")
        else:
            self.handle_error()

    def handle_oprd_id(self, pilha_sintatica):
        token, erro = self.get_id(pilha_sintatica)
        if not erro:
            self.pilha_semantica.append(token)

    def handle_oprd_num(self, pilha_sintatica):
        for el in pilha_sintatica:
            if isinstance(el, Token) and el.classe == "num":
                self.pilha_semantica.append(el)

    def handle_cond(self):
        self.code.append("}\n")

    def handle_cab(self):
        self.code.append(f"if ({self.pilha_semantica[-1].lexema}) {{\n")

    def handle_exp_r(self, pilha_sintatica):
        for el in pilha_sintatica:
            if isinstance(el, Token) and el.classe == "opr":
                opr = el
        opr1 = self.pilha_semantica[-2]
        opr2 = self.pilha_semantica[-1]
        if opr1.tipo == opr2.tipo:
            self.temp_count += 1
            self.pilha_semantica.append(Token("temp", f"T{self.temp_count}", opr1.tipo))
            self.code.append(f"T{self.temp_count} = {opr1.lexema} {opr.lexema} {opr2.lexema};\n")
        else:
            self.handle_error("Operandos com tipos incompatíveis")

    def handle_while(self):
        exp_r = self.pilha_semantica[-1]
        self.hold_temp_line = self.code[-1]
        self.code.append(f"while({exp_r.lexema}) {{\n")

    def handle_end_while(self):
        self.code.append(self.hold_temp_line)
        self.code.append("}")
        self.hold_temp_line = ""

    def semantic_action(self, rule, pilha_sintatica):
        action_map = {
            1: self.add_blank_lines,
            2: self.update_symbol_table,
            3: lambda: self.add_ids_to_symbol_table(pilha_sintatica),
            4: lambda: self.add_id_to_symbol_table(pilha_sintatica),
            5: lambda: self.save_current_type(pilha_sintatica),
            6: lambda: self.handle_leia(pilha_sintatica),
            7: self.handle_escreva,
            8: lambda: self.add_to_pilha_semantica(pilha_sintatica),
            9: lambda: self.handle_oprd_id(pilha_sintatica),
            10: lambda: self.handle_assign(pilha_sintatica),
            11: lambda: self.handle_ld(pilha_sintatica),
            13: lambda: self.handle_oprd_id(pilha_sintatica),
            14: lambda: self.handle_oprd_num(pilha_sintatica),
            15: self.handle_cond,
            16: self.handle_cab,
            17: lambda: self.handle_exp_r(pilha_sintatica),
            20: self.handle_while,
            24: self.handle_end_while
        }
        
        if rule in action_map:
            action_map[rule]()
        
                        
        
    def write_code(self):
        if self.error == False:
            def indent(level):
                return "    " * level

            indent_level = 0
            pre_code = []
            pre_code.append("#include<stdio.h>\n")
            pre_code.append("typedef char literal[256];\n")
            pre_code.append("void main(void) \n{\n")
            
            indent_level += 1
            pre_code.append(indent(indent_level) + "/*----Variaveis temporarias----*/\n")
            
            for el in self.pilha_semantica:
                if isinstance(el, Token):
                    if el.classe == "temp":
                        pre_code.append(indent(indent_level) + f"{traduz_tipo(el.tipo)} {el.lexema};\n")
            
            pre_code.append(indent(indent_level) + "/*------------------------------*/\n")
            
            for key in self.symbol_table.keys():
                pre_code.append(indent(indent_level) + traduz_tipo(self.symbol_table[key].tipo) + " " +self.symbol_table[key].lexema+";\n")
            
            for line in self.code:
                if "{" in line.strip():
                    pre_code.append(indent(indent_level) + line.strip() + "\n")
                    indent_level += 1
                elif "}" in line.strip():
                    indent_level -= 1
                    pre_code.append(indent(indent_level) + line.strip() + "\n")
                else:
                    if line != "\n\n\n":
                        pre_code.append(indent(indent_level) + line.strip() + "\n")
                    else:
                        pre_code.append(line)
            
            indent_level -= 1
            pre_code.append("}\n")
            
            with open(self.filename, "w") as file:
                file.write("".join(pre_code))
        else:
            print("Código não construído devido aos erros")
    

             

        


