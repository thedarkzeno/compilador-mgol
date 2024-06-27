class LR0Item:
    def __init__(self, lhs, rhs, dot_position=0):
        self.lhs = lhs
        self.rhs = rhs
        self.dot_position = dot_position

    def __eq__(self, other):
        return (self.lhs == other.lhs and
                self.rhs == other.rhs and
                self.dot_position == other.dot_position)

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs), self.dot_position))

    def __repr__(self):
        return f"{self.lhs} -> {' '.join(self.rhs[:self.dot_position] + ['.'] + self.rhs[self.dot_position:])}"

def closure(items, rules):
    closure_set = set(items)
    while True:
        new_items = set()
        for item in closure_set:
            if item.dot_position < len(item.rhs):
                symbol = item.rhs[item.dot_position]
                if symbol in rules:
                    for production in rules[symbol]:
                        new_items.add(LR0Item(symbol, production))
        if new_items.issubset(closure_set):
            break
        closure_set.update(new_items)
    return closure_set

def goto(items, symbol, rules):
    goto_set = set()
    for item in items:
        if item.dot_position < len(item.rhs) and item.rhs[item.dot_position] == symbol:
            goto_set.add(LR0Item(item.lhs, item.rhs, item.dot_position + 1))
    return closure(goto_set, rules)

def build_lr0_automaton(rules):
    start_symbol = list(rules.keys())[0]
    start_item = LR0Item(start_symbol, rules[start_symbol][0])
    start_state = closure({start_item}, rules)
    
    states = [start_state]
    transitions = {}
    state_map = {frozenset(start_state): 0}

    while True:
        new_states = []
        for state in states:
            for symbol in set(rules.keys()).union(set(item.rhs[item.dot_position] for item in state if item.dot_position < len(item.rhs))):
                new_state = goto(state, symbol, rules)
                if new_state and frozenset(new_state) not in state_map:
                    state_map[frozenset(new_state)] = len(states) + len(new_states)
                    new_states.append(new_state)
                    transitions[(state_map[frozenset(state)], symbol)] = state_map[frozenset(new_state)]
        if not new_states:
            break
        states.extend(new_states)

    return states, transitions

# Função para exibir o autômato LR(0)
def print_automaton(states, transitions):
    print("Estados:")
    for i, state in enumerate(states):
        print(f"I{i}: {state}")
    print("\nTransições:")
    for (state, symbol), next_state in transitions.items():
        print(f"I{state} -- {symbol} --> I{next_state}")