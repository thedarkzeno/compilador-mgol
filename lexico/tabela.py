estadoInicial = 0
estadoNum = 1
estadoNumPonto = 2
estadoNumExpoente1 = 3
estadoNumExpoente2 = 4
estadoNumExpoenteFinal = 5

estadoLiteral = 7
estadoLiteralFinal = 8
estadoId = 9
estadoComentario = 10
estadoComentarioFinal = 11
estadoOPM = 12
estadoOPRMenor = 13
estadoRCB = 14
estadoOPRMenorIgualDiferente = 15
estadoOPRMaior = 16
estadoOPRMaiorIgual = 17
estadoOPRIgual = 18
estadoABP = 19
estadoFCP = 20
estadoPTV = 2


tabela_de_transição = {
    estadoInicial: {
        "transitions": {
            "D": estadoNum,
            "L": estadoId
        },
        "final": False
    
    },
    estadoNum: {
        "transitions": {
            "D": estadoNum,
            ".": estadoNumPonto,
            "E,e": estadoNumExpoente1
        },
        "final": True
    },
    estadoNumPonto: {
        "transitions": {
            "D": estadoNumPonto,
            "E,e": estadoNumExpoente1   
        } ,
        "final": True
    },
    estadoNumExpoente1: {
        "transitions": {
            "+,-": estadoNumExpoente2,
            "D": estadoNumExpoenteFinal 
        },
        "final": False
    },
    estadoNumExpoente2: {
        "transitions": {
            "D": estadoNumExpoenteFinal 
        },
        "final": False
    },
    estadoNumExpoenteFinal: {
        "transitions": {
            "D": estadoNumExpoenteFinal 
        },
        "final": True
    },
    estadoId:{
        "transitions": {
            "L": estadoId,
            "D": estadoId,
            "_": estadoId
        },
        "final": True
    }
}

class AFD():
    def __init__(self):
        self.estadoInicial = estadoInicial
        self.estado = estadoInicial
        pass
    
    def e_digito(self, caracter):
        return caracter.isdigit()

    def e_letra(self, caracter):
        return caracter.isalpha() or caracter == '_'
    
    def transicao(self, caractere):
        _type = None
        if caractere == "+" or caractere == "-":
            _type = ("+,-")
        elif self.e_digito(caractere):
            _type = ("D")
        elif "E,e" in tabela_de_transição[self.estado]["transitions"] and caractere == "E" or caractere == "e":
            _type = "E,e"
        elif self.e_letra(caractere):
            _type = ("L")
        elif caractere == ".":
            _type = "."
        
            
        if _type in tabela_de_transição[self.estado]["transitions"]:
            self.estado = tabela_de_transição[self.estado]["transitions"][_type]
        else:
            print("no transition")
        print(_type, self.estado)
    
    def reset(self):
        self.estado = self.estadoInicial

if __name__ == "__main__":
    estado = AFD()
    estado.transicao("1")
    estado.transicao(".")
    estado.transicao("1")
    estado.transicao("E")
    estado.transicao("-")
    estado.transicao("5")
    
    estado.transicao("+")
    estado.transicao("a")
    estado.transicao("A")
    print(tabela_de_transição)