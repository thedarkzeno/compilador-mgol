from lexico import Scanner

scanner = Scanner()
with open("lexico/teste.mgol") as file:
    codigo = file.read()
tokens = []
while True:
    token = scanner.scanner(codigo)
    if token.classe == "EOF":
        break
    tokens.append(token)

for token in tokens:
    print(token)