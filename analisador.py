from .dfa import *

class Token:
    def __init__(self, classe, lexema, tipo):
        self.classe = classe
        self.lexema = lexema
        self.tipo = tipo

    def __str__(self):
        return f"Classe: {self.classe}, Lexema: '{self.lexema}', Tipo: {self.tipo}"

palavras_reservadas = {
    "inicio": Token("inicio", "inicio", "inicio"),
    "varinicio": Token("varinicio", "varinicio", "varinicio"),
    "varfim": Token("varfim", "varfim", "varfim"),
    "escreva": Token("escreva", "escreva", "escreva"),
    "leia": Token("leia", "leia", "leia"),
    "se": Token("se", "se", "se"),
    "entao": Token("entao", "entao", "entao"),
    "fimse": Token("fimse", "fimse", "fimse"),
    "repita": Token("repita", "repita", "repita"),
    "fimrepita": Token("fimrepita", "fimrepita", "fimrepita"),
    "fim": Token("fim", "fim", "fim"),
    "inteiro": Token("inteiro", "inteiro", "inteiro"),
    "literal": Token("literal", "literal", "literal"),
    "real": Token("real", "real", "real"),
}


def replace_letters_and_digits(s):
    result = ''
    length = len(s)

    i = 0
    while i < length:
        char = s[i]
        if char.isalpha():
            if (char in 'eE' and
                i > 0 and s[i-1].isdigit() and
                i+1 < length and (s[i+1].isdigit() or s[i+1] in '+-')):
                result += 'e'
                i += 1
                if s[i] in '+-':
                    result += s[i]
                    i += 1
                    while i < length and s[i].isdigit():
                        result += 'D'
                        i += 1
                    continue
            else:
                result += 'L'
        elif char.isdigit():
            result += 'D'
        else:
            result += char
        i += 1

    return result

def get_classe(state):
    classe = "?"
    if state.name == estadoLiteralFinal:
        classe = "Literal"
    elif state.name == estadoId:
        classe = "ID"
    elif state.name == estadoNum:
        classe = "Num"
    elif state.name == estadoNumPonto:
        classe = "Num"
    elif state.name == estadoNumExpoenteFinal:
        classe = "Num"
    elif state.name == estadoComentarioFinal:
        classe = "Comentario"
    elif state.name == estadoOPRFinal:
        classe = "OPR"
    elif state.name == estadoOPRMenor:
        classe = "OPR"
    elif state.name == estadoOPRMaior:
        classe = "OPR"
    elif state.name == estadoRCB:
        classe = "RCB"
    elif state.name == estadoOPM:
        classe = "OPM"
    elif state.name == estadoABP:
        classe = "ABP"
    elif state.name == estadoFCP:
        classe = "FCP"
    elif state.name == estadoVIR:
        classe = "VIR"
    elif state.name == estadoPTV:
        classe = "PTV"

    return classe

class Scanner():
    def __init__(self):
        self.name = "scanner"
        self.pos = 0
        self.linha = 0
        self.coluna = 0
        self.tabela_de_simbolos = palavras_reservadas
    
    def scanner(self, codigo_fonte):
        def ler_caractere():
            if self.pos < len(codigo_fonte):
                c = codigo_fonte[self.pos]
                self.pos += 1
                self.coluna += 1
                return c
            else:
                return None

        while True:
            c = ler_caractere()
            if c is None:
                break

            if c.isspace():
                if c == '\n':
                    self.linha += 1
                    self.coluna = 1
                continue

            lexema = c
            
            accepts, transitioned, state = dfa.accepts(replace_letters_and_digits(lexema))
            
            if not accepts:
                if transitioned == False:
                    print(f"ERRO LÉXICO: Sequência de números inválida '{lexema}' na linha {self.linha}, coluna {self.coluna}")
                    return Token("ERRO", lexema, "Nulo")

            classe = "?"
            tipo = "Nulo"
            while (c := ler_caractere()):
                new_lexema = lexema + c
                
                test_lexema = replace_letters_and_digits(new_lexema)
                if state.name == estadoNum or state.name == estadoNumPonto:
                    if c == "e" or c == "E":
                        test_lexema = replace_letters_and_digits(lexema)+c
                
                accepts, transitioned, state = dfa.accepts(test_lexema)

                if not accepts:
                    if transitioned == False:
                        self.pos -= 1
                        self.coluna -= 1
                        
                        classe = get_classe(state)
                        if classe == "ID":
                            token = self.tabela_de_simbolos.get(lexema, Token("ID", lexema, tipo))
                            if token.classe == "ID":
                                self.tabela_de_simbolos[token.lexema] = token
                            return token
                        classe = get_classe(state)
                        return Token(classe, lexema, tipo)
                lexema = new_lexema
            classe = get_classe(state)
            if classe == "ID":
                token = self.tabela_de_simbolos.get(lexema, Token(classe, lexema, tipo))
                if token.classe == "ID":
                    self.tabela_de_simbolos[token.lexema] = token
            return token

        return Token("EOF", "EOF", "EOF")

