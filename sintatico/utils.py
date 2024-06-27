import pandas as pd
from collections import defaultdict


# df = pd.read_csv("gramatica.csv")

# Função para extrair as regras gramaticais em forma de dicionário
def get_grammar_rules(df):
    rules = defaultdict(list)
    for _, row in df.iterrows():
        lhs, rhs = row['regra'].split('→')
        lhs = lhs.strip()
        rhs = [symbol.strip() for symbol in rhs.split()]
        rules[lhs].append(rhs)
    return rules

#falta adicionar os não terminais como first deles mesmos
# Função para calcular o conjunto FIRST
def compute_first(rules):
    first = defaultdict(set)
    
    def first_of(symbol):
        if symbol not in rules:  # Terminal
            return {symbol}
        if not first[symbol]:  # If not computed yet
            for production in rules[symbol]:
                for prod_symbol in production:
                    first[symbol].update(first_of(prod_symbol))
                    if 'ε' not in first[prod_symbol]:  # If ε is not in FIRST of the symbol
                        break
                    else:
                        first[symbol].add('ε')  # If all symbols in production can produce ε
        return first[symbol]
    
    # Initialize FIRST sets for terminals
    for non_terminal in rules:
        for production in rules[non_terminal]:
            for symbol in production:
                if symbol not in rules:  # It's a terminal
                    first[symbol] = {symbol}
                    
    for non_terminal in rules:
        first_of(non_terminal)
    
    return first

# Função para calcular o conjunto FOLLOW
def compute_follow(rules, first):
    follow = defaultdict(set)
    start_symbol = next(iter(rules))  # Assume the first non-terminal in the rules is the start symbol
    follow[start_symbol].add('$')  # Start symbol's follow set contains '$'

    def follow_of(symbol):
        if symbol not in follow:
            follow[symbol] = set()
        return follow[symbol]

    while True:
        updated = False
        for lhs, productions in rules.items():
            for production in productions:
                for i, B in enumerate(production):
                    if B in rules:  # B is a non-terminal
                        follow_B = follow_of(B)
                        first_rest = set()
                        for symbol in production[i + 1:]:
                            first_rest.update(first[symbol])
                            if 'ε' not in first[symbol]:
                                break
                        else:
                            first_rest.add('ε')

                        new_follow_B = (follow_B | (first_rest - {'ε'})) | (follow[lhs] if 'ε' in first_rest else set())
                        if new_follow_B != follow_B:
                            follow[B] = new_follow_B
                            updated = True
        if not updated:
            break

    return follow

# # Obter regras gramaticais
# rules = get_grammar_rules(df)
# # print(rules)

# # Calcular conjuntos FIRST e FOLLOW
# first = compute_first(rules)
# # print(first)
# follow = compute_follow(rules, first)

# # Exibir os resultados
# print("Conjuntos FIRST:")
# for non_terminal, first_set in first.items():
#     print(f"{non_terminal}: {first_set}")

# print("\nConjuntos FOLLOW:")
# for non_terminal, follow_set in follow.items():
#     print(f"{non_terminal}: {follow_set}")