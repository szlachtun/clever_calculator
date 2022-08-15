import re
import converter

variables = {}


class NextLoop(Exception):
    pass


def check_command(string):
    if string == '/help':
        print('The program calculates the sum of numbers')
        return True
    elif string == '/exit':
        print('Bye!')
        exit()
    elif re.match(r'\A */', string):
        print('Unknown command')
        raise NextLoop
    elif string == '':
        raise NextLoop
    else:
        return False


def is_assign(string):
    if string.count('=') == 0:  # Expression
        return False
    elif string.count('=') == 1:  # Assignment
        if re.match(r'\A *[A-z]+ *=', string):
            return True
        else:
            print('Invalid indentation')
            raise NextLoop
    else:
        print('Invalid assignment')
        raise NextLoop


def process_expr(string):
    parsed_vars = re.findall(r'\d?[A-Za-z]+', string)
    for parsed_var in parsed_vars:
        if parsed_var in variables.keys():
            string = string.replace(parsed_var, str(variables[parsed_var]))
        elif re.match(r'\d', parsed_var):
            print('Invalid assignment')
            raise NextLoop
        else:
            print('Unknown variable')
            raise NextLoop

    if string.count('(') != string.count(')') or re.findall(r'\*{2,}', string) or re.findall(r'/{2,}', string):
        print('Invalid expression')
        raise NextLoop

    string = re.sub(r' *- *', '-', re.sub(r' *\+ *', '+', string))
    string = re.sub(r'\++', '+', string.replace('--', '+')).replace('+-', '-').strip(' ')
    return converter.eval_rpn(converter.create_rpn(converter.prettify_expr(string)))


def run():
    while True:
        try:
            string = input()
            check_command(string)
            if is_assign(string):
                var = re.findall(r'[A-z]+', string)[0]
                string = re.sub(r'\A *[A-z]+ *=', '', string, 1)
                variables[var] = process_expr(string)
            else:
                print(process_expr(string))
        except NextLoop:
            continue


if __name__ == '__main__':
    run()
