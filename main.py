from lexico import Scanner
from sintatico import *
# scanner = Scanner()

# with open("lexico/teste.mgol") as file:
#     codigo = file.read()

# while True:
#     token = scanner.scanner(codigo)
    
#     if token.classe == "EOF":
#         break
    
#     print(token)

# Exemplo de uso:
if __name__ == "__main__":
    import pandas as pd
    
    # Carregar a gramática a partir de um arquivo CSV
    df = pd.read_csv('./sintatico/gramatica.csv')
    lr_table=pd.read_csv('./sintatico/lr_table.csv')
    print(lr_table)
    goto_table =pd.read_csv('./sintatico/goto.csv') 
    closure_table = pd.read_csv('./sintatico/estados_closure.csv')

    rules = get_grammar_rules(df)
    # first = compute_first(rules)
    # follow = compute_follow(rules, first)
    
    # states, transitions = build_lr0_automaton(rules)
    # print_automaton(states, transitions)
    # action_table, goto_table = build_slr_table(states, transitions, rules, first, follow)
    # print_slr_table(action_table, goto_table)

    scanner = Scanner()
    parser = Parser(lr_table, goto_table, df, scanner)
    
    with open("lexico/teste.mgol") as file:
        codigo = file.read()
    
    parser.parse(codigo)

