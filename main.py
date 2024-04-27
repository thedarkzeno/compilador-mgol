from lexico import Scanner

scanner = Scanner()

with open("lexico/teste.mgol") as file:
    codigo = file.read()

while True:
    token = scanner.scanner(codigo)
    
    if token.classe == "EOF":
        break
    
    print(token)

