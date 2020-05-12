def infix_to_postfix_regex(infix_regex):
    postfix_list, operator_stack = [], []

    for i, char in enumerate(infix_regex):

        if char in ['+', '&']:
            # If the operator stack is not empty and we encounter a new binary
            # operator, we push the existing binary operator into the queue
            # first, unless the existing operator is a left-bracket, which we
            # treat as the beginning of a new list.
            if operator_stack and operator_stack[-1] != '(':
                postfix_list.append(operator_stack.pop())
            operator_stack.append(char)

        elif char == '(':
            operator_stack.append(char)

        elif char == ')':
            try:
                if operator_stack[-1] != '(':
                    postfix_list.append(operator_stack.pop())
                operator_stack.pop()
            except IndexError:
                raise RuntimeError('Unmatched brackets')

        else:
            # This case handles both the unary operators and any literals,
            # which can both be added directly to the queue.
            postfix_list.append(char)

    # If there is an operator left on the stack, we pop it onto the queue.
    if operator_stack:
        postfix_list.append(operator_stack.pop())

    postfix_regex = ''.join(postfix_list)

    return postfix_regex


def add_concat_ops_to_regex(no_concat_regex):
    # Adds explicit concatenation operators to a regex.

    with_concat_list = []

    for i, char in enumerate(no_concat_regex):
        with_concat_list.append(char)

        # We only add concatenation operators between certain combinations of
        # characters.
        if (char not in ['(', '+']
                and i + 1 < len(no_concat_regex)
                and no_concat_regex[i + 1] not in ['*', '+', ')']):
            with_concat_list.append('&')

    with_concat_regex = ''.join(with_concat_list)

    return with_concat_regex


def get_postfix_regex(infix_regex):
    return infix_to_postfix_regex(add_concat_ops_to_regex(infix_regex))
