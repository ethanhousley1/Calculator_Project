from pair import *
from operator import add, sub, mul, truediv
def tokenize(expression):
    split_expression = expression.replace('(',' ( ').replace(')',' ) ').replace('/',' / ').replace('*', ' * ').replace('-',' - ').replace('+', ' + ')
    split_expression = split_expression.split()
    return split_expression
    
def parse_tokens(tokens, index):
    if tokens[index].isalpha():
        raise TypeError('no letters allowed!')
    if tokens[index].replace(' ','') == "(":
        operator = tokens[index+1]
        # step 1.2 on
        if index != 0:
            new_pair_list, index = parse_tokens(tokens, index+2)
            operator = Pair(operator, new_pair_list)
        if index == 0: # 1.3
            index += 2
        new_list, index = parse_tokens(tokens,index) # 1.4
        return Pair(operator, new_list), index
    if tokens[index].replace(' ','') == ")":
        return nil, index+1
    try:
        if '.' in tokens[index]:
            var = float(tokens[index])
        else:
            var = int(tokens[index])
    except:
        var = tokens[index]
    new_list, index = parse_tokens(tokens, index+1)
    return Pair(var, new_list), index
def parse(tokens):
    pair, index = parse_tokens(tokens, 0)
    return pair
def main():
    print('Welcome to the CS 111 Calculator Interpreter.')
    main_loop()
    print('Goodbye!')

def reduce(func, operands, initial):
    if operands is nil:
        return initial
    return reduce(func, operands.rest, func(initial, operands.first))

def apply(operator, operands):
    if operator == '+':
        return reduce(add, operands, 0)
    elif operator == '*':
        return reduce(mul, operands, 1)
    elif operator == '-':
        return reduce(sub, operands.rest, operands.first)
    elif operator =='/':
        return reduce(truediv, operands.rest, operands.first)
    else:
        raise TypeError
def eval(syntax_tree):
    if isinstance(syntax_tree, int) or isinstance(syntax_tree, float):
        return syntax_tree
    if isinstance(syntax_tree, Pair):
        operator = syntax_tree.first
        operands = nil
        current = syntax_tree.rest
        last = nil
        while current is not nil:
            evaluated_operand = eval(current.first)
            new_pair = Pair(evaluated_operand, nil)
            if operands is nil:
                operands = new_pair
            else:
                last.rest = new_pair
            last = new_pair
            current = current.rest

        results = apply(operator, operands)
        return results
    else:
        raise TypeError

def main_loop():
    while True:
        prompt = input('calc >> ')
        if prompt == 'exit':
            break
        # parse the string and validate it
        tokens = tokenize(prompt)
        try:
            pair_object= parse(tokens)
        except Exception as e:
            print(e)
        
        # if not print an error and restart the loop
        evaluation = eval(pair_object)
        print(evaluation)
        # evalute the parsed expression
        # print the result 
        # return to step 1

if __name__ == "__main__":
    main()