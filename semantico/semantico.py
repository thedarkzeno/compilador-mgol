from lexico import Token

def traduz_tipo(tipo):
    if tipo == "inteiro":
        return "int"
    if tipo == "real":
        return "double"
    if tipo == "literal":
        return "literal"


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.filename = "PROGRAMA.c"
        self.code = []
        self.error = False
        self.current_type = None
        self.arg = None

        self.pilha_semantica = []
        self.temp_count=0
    
    def get_id(self, pilha_sintatica):
        erro = False
        pilha = pilha_sintatica.copy()
        pilha.reverse()
        for el in pilha:
            if isinstance(el, Token):
                if el.classe == "id":
                    token = self.symbol_table.get(el.lexema, Token("id", el.lexema, "Nulo"))
                    if token.tipo == "Nulo":
                        print("Erro: Variável não declarada na linha tal")
                        erro = True
                    return token, erro
        return None, True
    
    def semantic_action(self, rule, pilha_sintatica):
        if (rule == 1):
            #varfim
            print("regra 1")
            # Imprimir três linhas brancas no arquivo objeto
            self.code.append("\n\n\n")
        
        elif rule == 2:
            #Amarração de atributos, organizar a passagem de valores do atributo TIPO.tipo, para L.TIPO;
            print("regra 2")
            if self.current_type != None:
                for key in self.symbol_table.keys():
                    # print(self.symbol_table[key].tipo)
                    if self.symbol_table[key].tipo == "Nulo":
                        self.symbol_table[key].tipo = self.current_type
                        

        
        elif rule == 3:
            print("regra 3")
            #Adicionar Ids separados por vírgula na tabela de símbolos
            for el in pilha_sintatica:
                if isinstance(el, Token):
                    if el.classe == "id":
                        token = self.symbol_table.get(el.lexema, Token("id", el.lexema, "Nulo"))
                        self.symbol_table[el.lexema] = token


                    
        elif rule == 4:
            # Inserir Id na tabela de simbolos
            print("regra 4")
            # print(pilha_sintatica)
            id = pilha_sintatica[-2]
            token = self.symbol_table.get(id.lexema, Token("id", id.lexema, "Nulo"))
            self.symbol_table[id.lexema] = token

            # self.code.append(" "+id.lexema+";\n")
            
            # for el in self.pilha_semantica:
            #     print(el)
            #     self.code[-1]+=(" "+el.lexema+",")
            # self.code[-1]+=(" "+id.lexema+";\n")
        
        elif rule == 5:
            print("regra 5")
            #TIPO.tipo <= inteiro.tipo
            token = pilha_sintatica[-2]
            tipo = (token.lexema)
            self.current_type = tipo

            
        elif rule == 6:
            print("regra 6")
            token, erro = self.get_id(pilha_sintatica)
            if not erro:
                if token.tipo == "literal":
                    self.code.append(f'scanf("%s", {token.lexema});\n')
                elif token.tipo == "inteiro":
                    self.code.append(f'scanf("%d",  &{token.lexema});\n')
                elif token.tipo == "real":
                    self.code.append(f'scanf("%lf",  &{token.lexema});\n')
        elif rule == 7:
            print("regra 7")
            # if self.arg:
            token = self.pilha_semantica[-1]
            lexema = token.lexema.replace('"', '')#self.arg.lexema.replace('"', '')
            print(token)
            if token.tipo == "lit":
                self.code.append(f'printf("{lexema}");\n')
            if token.tipo == "literal":
                self.code.append(f'printf("%s",{lexema});\n')
            if token.tipo == "inteiro":
                self.code.append(f'printf("%d",{lexema});\n')
            if token.tipo == "real":
                self.code.append(f'printf("%lf",{lexema});\n')
        elif rule == 8:
            print("regra 8")
            token = pilha_sintatica[-2]
            # print(token)
            # self.arg = token
            self.pilha_semantica.append(token)
        elif rule == 9:
            print("regra 9")
            token, erro = self.get_id(pilha_sintatica)
            if not erro:
                # self.arg = token
                self.pilha_semantica.append(token)
        elif rule == 10:
            #id rcb LD
            print("regra 10")
            temp = self.pilha_semantica[-1]
            token, erro = self.get_id(pilha_sintatica)
            print( temp, token)
            if not erro:
                #comparar tipos de temp e token
                if temp.tipo == token.tipo:
                    self.code.append(f"{token.lexema} = {temp.lexema};\n")
                else:
                    print("ERRO")
                print(token)
                # print("oprd", self.oprd)
        elif rule == 11:
            #LD→ OPRD opm OPRD 
            for el in pilha_sintatica:
                if isinstance(el, Token):
                    print(el)
                    opm = el
            print("regra 11")
            print(self.pilha_semantica[-1], self.pilha_semantica[-2])
            if (self.pilha_semantica[-1].tipo == self.pilha_semantica[-2].tipo) and self.pilha_semantica[-1].tipo != "literal":
                tipo = self.pilha_semantica[-1].tipo
                opm1 = self.pilha_semantica[-1]
                opm2 = self.pilha_semantica[-2]
                self.temp_count += 1
                for i in range(2):
                    self.pilha_semantica.pop()
                self.pilha_semantica.append(Token("temp", "T"+str(self.temp_count), tipo))
                self.code.append(f"T{self.temp_count} = {opm2.lexema} {opm.lexema} {opm1.lexema};\n")
                print(opm2, opm1)
            else:
                print("ERRO")
            pass
        elif rule == 13:
            #OPRD → id
            print("regra 13")
            #verificar se id é declarado
            token, erro = self.get_id(pilha_sintatica)
            if not erro:
                #receber oprd
                self.pilha_semantica.append(token)
                print(token)
                
        elif rule == 14:
            #OPRD → num
            print("regra 14")
            #verificar se id é declarado
            for el in pilha_sintatica:
                if isinstance(el, Token):
                    print(el)
                    if el.classe == "num":
                        token = el
                        #receber oprd
                        self.pilha_semantica.append(token)
                        print(token)
        elif rule == 15:
            #COND → CAB CP
            self.code.append("}\n")
        elif rule == 16:
            #CAB → se ab_p EXP_R fc_p então
            print("regra 16")
            # for el in pilha_sintatica:
            #     if isinstance(el, Token):
            #         print(el)
            self.code.append("if ("+str(self.pilha_semantica[-1].lexema)+") {\n")
        elif rule ==17:
            #XP_R → OPRD opr OPRD
            print("regra 17")
            for el in pilha_sintatica:
                if isinstance(el, Token):
                    if el.classe == "opr":
                        opr = el
            opr1 = self.pilha_semantica[-2]
            opr2 = self.pilha_semantica[-1]
            #Verificar se os tipos de dados de OPRD são iguais ou equivalentes para a realização de comparação relacional.
            if opr1.tipo == opr2.tipo:
                # print("okay")
                self.temp_count += 1
                self.pilha_semantica.append(Token("temp", "T"+str(self.temp_count), opr1.tipo))
                self.code.append(f"T{self.temp_count} = {opr1.lexema} {opr.lexema} {opr2.lexema};\n")
            else:
                print("Erro: Operandos com tipos incompatíveis, linha e coluna")
        elif rule == 20:
            print("regra", 20)
            #CABR → repita ab_p EXP_R fc_p
            print("pilha sintatica")
            for el in pilha_sintatica:
                print(el)
            
            EXP_R = self.pilha_semantica[-1]
            self.code.append(f"while({EXP_R.lexema})" + "{\n")
        elif rule == 24:
            print("regra", 24)
            #CPR → fimrepita
            self.code.append("}")
                        
        
    def write_code(self):
        def indent(level):
            return "    " * level  # 4 spaces per indentation level

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

             

        


