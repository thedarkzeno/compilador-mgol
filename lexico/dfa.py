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

stateInicial = "q0"
stateNum = "q1"
stateNumPonto = "q2"
stateNumExpoente1 = "q3"
stateNumExpoente2 = "q4"
stateNumExpoenteFinal = "q5"

stateLiteral = "q6"
stateLiteralFinal = "q7"

stateId = "q8"

stateComentario = "q9"
stateComentarioFinal = "q10"

stateEOF = "q11"

stateOPRMenor = "q12"
stateRCB = "q13"
stateOPRMaior = "q14"
stateOPRFinal = "q15"

stateOPM = "q16"

stateABP = "q17"
stateFCP = "q18"
stateVIR = "q19"
statePTV = "q20"

transicao_curinga = "#"

dfa = DFA()
dfa.add_state(stateInicial, is_final=False)  

dfa.add_state(stateNum, is_final=True)  
dfa.add_state(stateNumPonto, is_final=True)  
dfa.add_state(stateNumExpoente1, is_final=False)  
dfa.add_state(stateNumExpoente2, is_final=False)  
dfa.add_state(stateNumExpoenteFinal, is_final=True)  

dfa.add_state(stateLiteral, is_final=False)  
dfa.add_state(stateLiteralFinal, is_final=True)  

dfa.add_state(stateId, is_final=True)  

dfa.add_state(stateComentario, is_final=False)  
dfa.add_state(stateComentarioFinal, is_final=True)  

dfa.add_state(stateEOF, is_final=True)  

dfa.add_state(stateOPRMenor, is_final=True)  
dfa.add_state(stateRCB, is_final=True)  
dfa.add_state(stateOPRMaior, is_final=True)  
dfa.add_state(stateOPRFinal, is_final=True)  

dfa.add_state(stateOPM, is_final=True)  

dfa.add_state(stateABP, is_final=True)  
dfa.add_state(stateFCP, is_final=True)  
dfa.add_state(stateVIR, is_final=True)  
dfa.add_state(statePTV, is_final=True)  





dfa.set_initial_state(stateInicial)

dfa.add_transition(stateInicial, 'D', stateNum)
dfa.add_transition(stateInicial, 'L', stateId)

dfa.add_transition(stateNum, 'D', stateNum)
dfa.add_transition(stateNum, '.', stateNumPonto)
dfa.add_transition(stateNum, 'E', stateNumExpoente1)
dfa.add_transition(stateNum, 'e', stateNumExpoente1)

dfa.add_transition(stateNumPonto, 'D', stateNumPonto)
dfa.add_transition(stateNumPonto, 'E', stateNumExpoente1)
dfa.add_transition(stateNumPonto, 'e', stateNumExpoente1)

dfa.add_transition(stateNumExpoente1, 'D', stateNumExpoenteFinal)
dfa.add_transition(stateNumExpoente1, '+', stateNumExpoente2)
dfa.add_transition(stateNumExpoente1, '-', stateNumExpoente2)

dfa.add_transition(stateNumExpoente2, 'D', stateNumExpoenteFinal)

dfa.add_transition(stateNumExpoenteFinal, 'D', stateNumExpoenteFinal)

dfa.add_transition(stateId, 'L', stateId)
dfa.add_transition(stateId, 'D', stateId)
dfa.add_transition(stateId, '_', stateId)

dfa.add_transition(stateInicial, '"', stateLiteral)
dfa.add_transition(stateLiteral, transicao_curinga, stateLiteral)
dfa.add_transition(stateLiteral, '"', stateLiteralFinal)

dfa.add_transition(stateInicial, '{', stateComentario)
dfa.add_transition(stateComentario, transicao_curinga, stateComentario)
dfa.add_transition(stateComentario, '}', stateComentarioFinal)

dfa.add_transition(stateInicial, 'EOF', stateEOF)

dfa.add_transition(stateInicial, '<', stateOPRMenor)
dfa.add_transition(stateOPRMenor, '-', stateRCB)
dfa.add_transition(stateOPRMenor, '>', stateOPRFinal)
dfa.add_transition(stateOPRMenor, '=', stateOPRFinal)
dfa.add_transition(stateInicial, '>', stateOPRMaior)
dfa.add_transition(stateOPRMaior, '=', stateOPRFinal)
dfa.add_transition(stateInicial, '=', stateOPRFinal)

dfa.add_transition(stateInicial, '+', stateOPM)
dfa.add_transition(stateInicial, '-', stateOPM)
dfa.add_transition(stateInicial, '*', stateOPM)
dfa.add_transition(stateInicial, '/', stateOPM)

dfa.add_transition(stateInicial, '(', stateABP)
dfa.add_transition(stateInicial, ')', stateFCP)
dfa.add_transition(stateInicial, ';', statePTV)
dfa.add_transition(stateInicial, ',', stateVIR)


if __name__ == "__main__":
    print(dfa.accepts('"LLL'))
    print(dfa.accepts('"LLL"'))