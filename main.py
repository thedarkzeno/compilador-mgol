from lexico import Scanner

scanner = Scanner()

with open("lexico/teste.mgol") as file:
    codigo = file.read()

while True:
    token = scanner.scanner(codigo)
    
    if token.classe == "EOF":
        break
    
    print(token)

# Opcional: exibir a tabela de símbolos final, para ver a adição dos IDs
# print("\nTabela de símbolos final:\n")
# for i in scanner.tabela_de_simbolos:
#     print(f"{i}: {scanner.tabela_de_simbolos[i]}")
