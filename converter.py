from collections import deque


def prettify_expr(infix):
    infix_list = []
    temp_num = ''
    for char in infix:
        if char.isdigit():
            temp_num += char
        elif temp_num != '':
            infix_list.append(temp_num)
            infix_list.append(char)
            temp_num = ''
        else:
            infix_list.append(char)
    if temp_num != '':
        infix_list.append(temp_num)
    return infix_list


def create_rpn(infix_list):
    output = ''
    op_stack = deque()
    for token in infix_list:
        if token.isdigit():
            output += token + ' '
        elif token in '^':
            op_stack.appendleft(token)
        elif token in '*/':
            if len(op_stack) > 0 and op_stack[0] in '^*/':
                while op_stack:
                    output += op_stack.popleft() + ' '
            op_stack.appendleft(token)
        elif token in '+-':
            if op_stack and op_stack[0] in '^*/+-':
                while op_stack:
                    output += op_stack.popleft() + ' '
            op_stack.appendleft(token)
        elif token in '(':
            op_stack.appendleft(token)
        elif token in ')':
            while op_stack[0] != '(':
                output += op_stack.popleft() + ' '
            op_stack.popleft()
    while op_stack:
        output += op_stack.popleft() + ' '
    return output[:-1].split(' ')


def eval_rpn(tokens):
    stack = deque()
    operators = {'+', '-', '*', '/', '^'}
    if len(tokens) == 1:
        return int(tokens[0])
    for token in tokens:
        if token not in operators:
            stack.append(int(token))
        else:
            sec_operand = stack.pop()
            fir_operand = stack.pop()
            tmp = 0
            if token == '+':
                tmp = fir_operand + sec_operand
            elif token == '-':
                tmp = fir_operand - sec_operand
            elif token == '*':
                tmp = fir_operand * sec_operand
            elif token == '/':
                tmp = int(fir_operand / sec_operand)
            elif token == '^':
                tmp = fir_operand ** sec_operand
            stack.append(tmp)
    return stack.pop()
