from dfa import *

class Token:
    def __init__(self, classe, lexema, tipo):
        self.classe = classe
        self.lexema = lexema
        self.tipo = tipo

    def __str__(self):
        return f"Classe: {self.classe}, Lexema: '{self.lexema}', Tipo: {self.tipo}"

palavras_reservadas = {
    "inicio": Token("inicio", "inicio", None),
    "varinicio": Token("varinicio", "varinicio", None),
    "varfim": Token("varfim", "varfim", None),
    "escreva": Token("escreva", "escreva", None),
    "leia": Token("leia", "leia", None),
    "se": Token("se", "se", None),
    "entao": Token("entao", "entao", None),
    "fimse": Token("fimse", "fimse", None),
    "repita": Token("repita", "repita", None),
    "fimrepita": Token("fimrepita", "fimrepita", None),
    "fim": Token("fim", "fim", None),
    "inteiro": Token("inteiro", "inteiro", "inteiro"),
    "literal": Token("literal", "literal", "literal"),
    "real": Token("real", "real", "real"),
}

# def busca_tabela(lexema):
#     return palavras_reservadas.get(lexema)

# def inserir_tabela(token):
#     if token.classe == "id":
#         palavras_reservadas[token.lexema] = token


# def replace_letters_and_digits(s):
#     # Create an empty result string
#     result = ''
    
#     # Iterate over each character in the input string
#     for char in s:
#         # Check if the character is a lowercase letter
#         if char.isalpha():
#             result += 'L'
#         # Check if the character is a digit
#         elif char.isdigit():
#             result += 'D'
#         # If neither, append the character as it is
#         else:
#             result += char
            
#     return result

def replace_letters_and_digits(s):
    result = ''
    length = len(s)

    i = 0
    while i < length:
        char = s[i]
        # Checa se é uma letra
        if char.isalpha():
            # Verifica se é um 'e' ou 'E' que faz parte de uma notação científica
            if (char in 'eE' and
                i > 0 and s[i-1].isdigit() and
                i+1 < length and (s[i+1].isdigit() or s[i+1] in '+-')):
                result += 'e'  # Mantém 'e' para notação científica
                i += 1
                # Pular o próximo caractere se for sinal, pois faz parte da notação
                if s[i] in '+-':
                    result += s[i]
                    i += 1
                    # Continua para adicionar dígitos após o sinal
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
                break  # Fim do arquivo

            # Ignora espaços e gerencia quebras de linha
            if c.isspace():
                if c == '\n':
                    self.linha += 1
                    self.coluna = 1
                continue

            # Inicializa o lexema com o primeiro caractere
            lexema = c
            
            accepts, transitioned, state = dfa.accepts(replace_letters_and_digits(lexema))
            
            if not accepts:
                print(f"ERRO LÉXICO: Sequência de números inválida '{lexema}' na linha {self.linha}, coluna {self.coluna}")
                return Token("ERRO", lexema, "NULO")

            # Identifica números (inteiros simples)
            classe = "?"
            tipo = "nulo"
            while (c := ler_caractere()):
                # print(c)
                new_lexema = lexema + c
                
                test_lexema = replace_letters_and_digits(new_lexema)
                
                accepts, transitioned, state = dfa.accepts(test_lexema)

                if not accepts:
                    if transitioned == False:
                        self.pos -= 1
                        self.coluna -= 1
                        
                        if state.name == estadoId:
                            token = self.tabela_de_simbolos.get(lexema, Token("ID", lexema, "nulo"))
                            if token.classe == "ID":
                                self.tabela_de_simbolos[token.lexema] = token
                            return token
                        return Token(classe, lexema, tipo)
                lexema = new_lexema
            return Token(classe, lexema, tipo)

        return Token("EOF", "EOF", "NULO")

