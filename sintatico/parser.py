class Parser:
    def __init__(self, action_table, goto_table, scanner):
        self.action_table = action_table
        self.goto_table = goto_table
        self.scanner = scanner
        self.stack = [0]

    def parse(self, codigo):
        index = 0
        token = self.scanner.scanner(codigo)
        print("token", token)
        while True:
            state = self.stack[-1]
            action = self.action_table[state].get(token.classe)
            print("action", action)
            print("state", state)
            print(self.action_table[state])
            if action is None:
                self.error_recovery()
                return
            elif action.startswith('shift'):
                next_state = int(action.split()[1])
                self.stack.append(token)
                self.stack.append(next_state)
                token = self.scanner.scanner(codigo)
                print(token)
            elif action.startswith('reduce'):
                production = action.split()[1].split('->')
                lhs = production[0].strip()
                rhs = production[1].strip().split()
                for _ in range(len(rhs) * 2):  # Pop both token and state for each symbol in rhs
                    self.stack.pop()
                state = self.stack[-1]
                next_state = self.goto_table[state][lhs]
                self.stack.append(lhs)
                self.stack.append(next_state)
                print(f"Reducing by: {lhs} -> {' '.join(rhs)}")
            elif action == 'accept':
                print("Accepted")
                return
            else:
                self.error_recovery()
                return

    def error_recovery(self):
        print("Syntax error")