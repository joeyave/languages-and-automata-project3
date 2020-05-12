import json


class Regex:
    def __init__(self, postfix_regex):
        self.alphabet = []

        # A stack of pairs of states, representing the input and output states of NFA.
        pair_states_stack = []

        for char in postfix_regex:
            if char == '&':
                (b_in, b_out), (a_in, a_out) = pair_states_stack.pop(), pair_states_stack.pop()
                a_out.add_transition('eps', b_in)
                pair_states_stack.append((a_in, b_out))

            elif char == '+':
                (b_in, b_out), (a_in, a_out) = pair_states_stack.pop(), pair_states_stack.pop()
                a_in.add_transition('eps', b_in)
                b_out.add_transition('eps', a_out)
                pair_states_stack.append((a_in, a_out))

            elif char == '*':
                (a_in, a_out) = pair_states_stack.pop()
                a_out.add_transition('eps', a_in)
                b_in, b_out = State(), State()
                b_in.add_transition("eps", a_in)
                b_in.add_transition("eps", b_out)
                a_out.add_transition("eps", b_out)
                pair_states_stack.append((b_in, b_out))
            elif char == "ϵ":
                a_in, a_out = State(), State()
                a_in.add_transition("eps", a_out)
                pair_states_stack.append((a_in, a_out))
            else:
                if char not in self.alphabet:
                    self.alphabet.append(char)
                a_in, a_out = State(), State()
                a_in.add_transition(char, a_out)
                pair_states_stack.append((a_in, a_out))

        self.initial_state, self.accepting_state = pair_states_stack.pop()

    def get_transitions(self, state, visited=[]):
        transitions = dict()
        if state not in visited:
            visited.append(state)

            for (value, connected_state) in state.transitions:
                transitions.update(self.get_transitions(connected_state))

                if (str(id(state)), value) in transitions:
                    transitions[(str(id(state)), value)].append(str(id(connected_state)))
                else:
                    transitions[(str(id(state)), value)] = [str(id(connected_state))]
        return transitions

    def convert_to_nfa(self, file_name):
        nfa = dict()
        nfa["alphabet"] = self.alphabet
        nfa["initial_state"] = str(id(self.initial_state))
        nfa["accepting_states"] = [str(id(self.accepting_state))]
        nfa["transitions"] = []
        transitions = self.get_transitions(self.initial_state)
        for key, value in transitions.items():
            nfa["transitions"].append([key[0], key[1], value])

        with open(file_name, 'w') as f:
            json.dump(nfa, f)


class State:
    def __init__(self):
        self.transitions = set()

    def add_transition(self, value, state):
        self.transitions.add((value, state))