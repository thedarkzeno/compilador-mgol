from lexico import Scanner
from sintatico import *
import pandas as pd

if __name__ == "__main__":

    gramatica = pd.read_csv("./sintatico/gramatica.csv")
    action_table = pd.read_csv("./sintatico/action.csv")
    goto_table = pd.read_csv("./sintatico/goto.csv")

    scanner = Scanner()
    parser = Parser(action_table, goto_table, gramatica, scanner)

    with open("lexico/teste.mgol") as file:
        codigo = file.read()

    parser.parse(codigo)
