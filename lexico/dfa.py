class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state

class DFA:
    def __init__(self):
        self.states = {}
        self.initial_state = None
        self.accept_states = set()

    def add_state(self, name, is_final=False):
        state = State(name)
        self.states[name] = state
        if is_final:
            self.accept_states.add(state)

    def set_initial_state(self, name):
        self.initial_state = self.states[name]

    def add_transition(self, from_state, symbol, to_state):
        self.states[from_state].add_transition(symbol, self.states[to_state])

    def accepts(self, string):
        current_state = self.initial_state
        for symbol in string:
            if symbol in current_state.transitions:
                
                current_state = current_state.transitions[symbol]
            else:
                if transicao_curinga in current_state.transitions:
                    current_state = current_state.transitions[transicao_curinga]
                else:
                    return False, False, current_state
        return current_state in self.accept_states, True, current_state

estadoInicial = "q0"
estadoNum = "q1"
estadoNumPonto = "q2"
estadoNumExpoente1 = "q3"
estadoNumExpoente2 = "q4"
estadoNumExpoenteFinal = "q5"

estadoLiteral = "q6"
estadoLiteralFinal = "q7"

estadoId = "q8"

estadoComentario = "q9"
estadoComentarioFinal = "q10"

estadoEOF = "q11"

estadoOPRMenor = "q12"
estadoRCB = "q13"
estadoOPRMaior = "q14"
estadoOPRFinal = "q15"

estadoOPM = "q16"

estadoABP = "q17"
estadoFCP = "q18"
estadoVIR = "q19"
estadoPTV = "q20"

transicao_curinga = "#"

dfa = DFA()
dfa.add_state(estadoInicial, is_final=False)  

dfa.add_state(estadoNum, is_final=True)  
dfa.add_state(estadoNumPonto, is_final=True)  
dfa.add_state(estadoNumExpoente1, is_final=False)  
dfa.add_state(estadoNumExpoente2, is_final=False)  
dfa.add_state(estadoNumExpoenteFinal, is_final=True)  

dfa.add_state(estadoLiteral, is_final=False)  
dfa.add_state(estadoLiteralFinal, is_final=True)  

dfa.add_state(estadoId, is_final=True)  

dfa.add_state(estadoComentario, is_final=False)  
dfa.add_state(estadoComentarioFinal, is_final=True)  

dfa.add_state(estadoEOF, is_final=True)  

dfa.add_state(estadoOPRMenor, is_final=True)  
dfa.add_state(estadoRCB, is_final=True)  
dfa.add_state(estadoOPRMaior, is_final=True)  
dfa.add_state(estadoOPRFinal, is_final=True)  

dfa.add_state(estadoOPM, is_final=True)  

dfa.add_state(estadoABP, is_final=True)  
dfa.add_state(estadoFCP, is_final=True)  
dfa.add_state(estadoVIR, is_final=True)  
dfa.add_state(estadoPTV, is_final=True)  






dfa.set_initial_state(estadoInicial)

dfa.add_transition(estadoInicial, 'D', estadoNum)
dfa.add_transition(estadoInicial, 'L', estadoId)

dfa.add_transition(estadoNum, 'D', estadoNum)
dfa.add_transition(estadoNum, '.', estadoNumPonto)
dfa.add_transition(estadoNum, 'E', estadoNumExpoente1)
dfa.add_transition(estadoNum, 'e', estadoNumExpoente1)

dfa.add_transition(estadoNumPonto, 'D', estadoNumPonto)
dfa.add_transition(estadoNumPonto, 'E', estadoNumExpoente1)
dfa.add_transition(estadoNumPonto, 'e', estadoNumExpoente1)

dfa.add_transition(estadoNumExpoente1, 'D', estadoNumExpoenteFinal)
dfa.add_transition(estadoNumExpoente1, '+', estadoNumExpoente2)
dfa.add_transition(estadoNumExpoente1, '-', estadoNumExpoente2)

dfa.add_transition(estadoNumExpoente2, 'D', estadoNumExpoenteFinal)

dfa.add_transition(estadoNumExpoenteFinal, 'D', estadoNumExpoenteFinal)

dfa.add_transition(estadoId, 'L', estadoId)
dfa.add_transition(estadoId, 'D', estadoId)
dfa.add_transition(estadoId, '_', estadoId)

dfa.add_transition(estadoInicial, '"', estadoLiteral)
dfa.add_transition(estadoLiteral, transicao_curinga, estadoLiteral)
dfa.add_transition(estadoLiteral, '"', estadoLiteralFinal)

dfa.add_transition(estadoInicial, '{', estadoComentario)
dfa.add_transition(estadoComentario, transicao_curinga, estadoComentario)
dfa.add_transition(estadoComentario, '}', estadoComentarioFinal)

dfa.add_transition(estadoInicial, 'EOF', estadoEOF)

dfa.add_transition(estadoInicial, '<', estadoOPRMenor)
dfa.add_transition(estadoOPRMenor, '-', estadoRCB)
dfa.add_transition(estadoOPRMenor, '>', estadoOPRFinal)
dfa.add_transition(estadoOPRMenor, '=', estadoOPRFinal)
dfa.add_transition(estadoInicial, '>', estadoOPRMaior)
dfa.add_transition(estadoOPRMaior, '=', estadoOPRFinal)
dfa.add_transition(estadoInicial, '=', estadoOPRFinal)

dfa.add_transition(estadoInicial, '+', estadoOPM)
dfa.add_transition(estadoInicial, '-', estadoOPM)
dfa.add_transition(estadoInicial, '*', estadoOPM)
dfa.add_transition(estadoInicial, '/', estadoOPM)

dfa.add_transition(estadoInicial, '(', estadoABP)
dfa.add_transition(estadoInicial, ')', estadoFCP)
dfa.add_transition(estadoInicial, ';', estadoPTV)
dfa.add_transition(estadoInicial, ',', estadoVIR)


if __name__ == "__main__":
    print(dfa.accepts('"LLL'))
    print(dfa.accepts('"LLL"'))