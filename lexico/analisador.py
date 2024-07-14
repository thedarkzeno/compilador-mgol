from .dfa import *


class Token:
    def __init__(self, classe, lexema, tipo):
        self.classe = classe
        self.lexema = lexema
        self.tipo = tipo

    def __str__(self):
        return f"Classe: {self.classe}, Lexema: '{self.lexema}', Tipo: {self.tipo}"

    def __eq__(self, other):
        if isinstance(other, Token):
            return (
                self.classe == other.classe
                and self.lexema == other.lexema
                and self.tipo == other.tipo
            )
        return False


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


def get_classe(state):
    classe = "?"
    if state.name == stateLiteralFinal:
        classe = "lit"
    elif state.name == stateId:
        classe = "id"
    elif state.name == stateNum:
        classe = "num"
    elif state.name == stateNumPonto:
        classe = "num"
    elif state.name == stateNumExpoenteFinal:
        classe = "num"
    elif state.name == stateComentarioFinal:
        classe = "Comentario"
    elif state.name == stateOPRFinal:
        classe = "opr"
    elif state.name == stateOPRMenor:
        classe = "opr"
    elif state.name == stateOPRMaior:
        classe = "opr"
    elif state.name == stateRCB:
        classe = "rcb"
    elif state.name == stateOPM:
        classe = "opm"
    elif state.name == stateABP:
        classe = "ab_p"
    elif state.name == stateFCP:
        classe = "fc_p"
    elif state.name == stateVIR:
        classe = "vir"
    elif state.name == statePTV:
        classe = "pt_v"

    return classe


def get_tipo(state):
    tipo = "Nulo"
    if state.name == stateNum:
        tipo = "inteiro"
    elif state.name in [
        stateNumPonto,
        stateNumExpoente1,
        stateNumExpoente2,
        stateNumExpoenteFinal,
    ]:
        tipo = "real"
    elif state.name == stateLiteralFinal:
        tipo = "lit"
    elif state.name == stateComentarioFinal:
        tipo = "comentario"
    return tipo


class Scanner:
    def __init__(self):
        self.name = "scanner"
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        self.tabela_de_simbolos = palavras_reservadas
        self.ended = False

    def get_token(self, lexema, state) -> Token:
        classe = get_classe(state)
        tipo = get_tipo(state)
        token = self.tabela_de_simbolos.get(lexema, Token(classe, lexema, tipo))
        if token.classe == "id":
            self.tabela_de_simbolos[token.lexema] = token
        return token

    def scanner(self, codigo_fonte):
        if self.ended == True:
            return Token("EOF", "EOF", "EOF")

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
                if c == "\n":
                    self.linha += 1
                    self.coluna = 1
                continue

            lexema = c

            accepts, transitioned, state = dfa.accepts(lexema)

            if not accepts:
                if transitioned == False:
                    print(
                        f"ERRO LÉXICO: Sequência de caracteres inválida na linguagem: '{lexema}', linha {self.linha}, coluna {self.coluna}"
                    )
                    return Token("ERRO", lexema, "Nulo")

            while c := ler_caractere():
                new_lexema = lexema + c

                accepts, transitioned, state = dfa.accepts(new_lexema)

                if not accepts:
                    if transitioned == False:
                        self.pos -= 1
                        self.coluna -= 1

                        token = self.get_token(lexema, state)
                        if token.classe == "Comentario":
                            break
                        return token

                lexema = new_lexema

            accepts, transitioned, state = dfa.accepts(lexema)
            if accepts:
                token = self.get_token(lexema, state)
                if token.classe != "Comentario":
                    return token
            else:
                print(
                    f"ERRO LÉXICO: Sequência de caracteres inválida na linguagem: '{lexema}', linha {self.linha}, coluna {self.coluna}"
                )
                return Token("ERRO", lexema, "Nulo")
        self.ended = True
        return Token("EOF", "EOF", "EOF")
