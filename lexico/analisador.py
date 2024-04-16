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

            # Reconhecer espaços, saltos de linha, etc.
            if c.isspace():
                if c == '\n':
                    self.linha += 1
                    self.coluna = 1
                continue

            # Reconhecer números
            if c.isdigit():
                lexema = c
                while (c := ler_caractere()) and c.isdigit():
                    lexema += c
                return Token("NUM", lexema, "inteiro")

            # Reconhecer identificadores e palavras reservadas
            if c.isalpha() or c == '_':
                lexema = c
                while (c := ler_caractere()) and (c.isalnum() or c == '_'):
                    lexema += c
                token = self.tabela_de_simbolos.get(lexema, Token("ID", lexema, "nulo"))
                
                if token.classe == "ID":
                    self.tabela_de_simbolos[token.lexema] = token
                
                return token

            # Outros caracteres e tokens
            # Implementar reconhecimento de outros tokens aqui

            # Erro léxico
            print(f"ERRO LÉXICO: Caractere inválido '{c}' na linha {self.linha}, coluna {self.coluna}")
            return Token("ERRO", "NULO", "NULO")

        return Token("EOF", "EOF", "NULO")

