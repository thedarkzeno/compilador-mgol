from collections import defaultdict

def build_slr_table(states, transitions, rules, first, follow):
    action_table = defaultdict(dict)
    goto_table = defaultdict(dict)

    for state_idx, state in enumerate(states):
        for item in state:
            if item.dot_position == len(item.rhs):
                if item.lhs == list(rules.keys())[0] and item.rhs == rules[item.lhs][0]:
                    action_table[state_idx]['$'] = 'accept'
                else:
                    for terminal in follow[item.lhs]:
                        if terminal not in action_table[state_idx] or action_table[state_idx][terminal].startswith('reduce'):
                            action_table[state_idx][terminal] = f"reduce {item.lhs} -> {' '.join(item.rhs)}"
            else:
                symbol = item.rhs[item.dot_position]
                if symbol in rules:
                    goto_table[state_idx][symbol] = transitions.get((state_idx, symbol))
                else:
                    next_state = transitions.get((state_idx, symbol))
                    if next_state is not None:
                        action_table[state_idx][symbol] = f"shift {next_state}"

    return action_table, goto_table

def print_slr_table(action_table, goto_table):
    print("ACTION Table:")
    for state, actions in action_table.items():
        for symbol, action in actions.items():
            print(f"ACTION[{state}, {symbol}] = {action}")

    print("\nGOTO Table:")
    for state, gotos in goto_table.items():
        for symbol, next_state in gotos.items():
            print(f"GOTO[{state}, {symbol}] = {next_state}")