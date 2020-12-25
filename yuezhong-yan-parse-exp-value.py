'''
This program implements a recursive descent parser for the CFG below:

The grammar has added pi and unary minus to the previous program.
Also, the parse function is now called in a loop, so you can evaluate
one expression after another.
------------------------------------------------------------
1 <exp> → <term>{+<term> | -<term>}
2 <term> → <factor>{*<factor> | /<factor>}
3 <factor> → <number> | pi | -<factor> | (<exp>) | <func>
4 <func> → <func name>(<exp>)
5 <func name> → sin | cos | tan | exp | sqrt | abs
6 <statement> → <id> = <exp>
'''
import math

class ParseError(Exception): pass

#==============================================================
# FRONT END PARSER
#==============================================================

i = 0  # keeps track of what character we are currently reading.
err = None

# A table to store symbols, where the key values are the identifiers, and the
# values are the expression values.
symbol_table = {}

# ---------------------------------------
# Parse an Expression   <exp> → <term>{+<term> | -<term>}
#
def exp():
    global i, err, parenthesis_in_stack, sub_parenthesis

    value = term()
    while True:
        if w[i] == '+':
            i += 1
            value = binary_op('+', value, term())
        elif w[i] == '-':
            i += 1
            value = binary_op('-', value, term())
        elif w[i] == ')': # Handle close parenthesis, check if (<exp>) is valid.
            i += 1
            parenthesis_in_stack -= 1

            # Handle unbalanced parentheses
            if sub_parenthesis < parenthesis_in_stack or parenthesis_in_stack < 0:
                print('unbalanced parentheses')
                raise ParseError

            sub_parenthesis = parenthesis_in_stack
            break
        else:
            break

    return value
# ---------------------------------------
# Parse a Term   <term> → <factor>{+<factor> | -<factor>}
#
def term():
    global i, err

    value = factor()
    while True:
        if w[i] == '*':
            i += 1
            value = binary_op('*', value, factor())
        elif w[i] == '/':
            i += 1
            value = binary_op('/', value, factor())
        else:
            break

    return value
# ---------------------------------------
# Parse a Factor   <factor> → (<exp>) | <number>
#
def factor():
    global i, err, parenthesis_in_stack, sub_parenthesis
    value = None

    if w[i] == 'pi':
        i += 1
        return math.pi
    elif w[i] == '-':
        i += 1
        return -factor()
    elif w[i] == '(': # Handle open parenthesis, if detect <exp>, then go to <exp>
        i += 1
        sub_parenthesis = parenthesis_in_stack
        parenthesis_in_stack += 1
        return exp()
    elif w[i].isdigit() == 0 and w[i] not in symbol_table:
        function_name = w[i]
        i += 1
        return func(function_name)
    else:
        try:
            value = atomic(w[i])
            i += 1          # read the next character
        except ValueError:
            print('number expected')
            value = None

    #print('factor returning', value)

    if value == None: raise ParseError
    return value
# ---------------------------------------
# Parse a Function   <func> → <func name>(<exp>)
#                    <func name> → sin | cos | tan | exp | sqrt | abs
#
def func(func_name):
    global i, err, parenthesis_in_stack, sub_parenthesis
    expression = None

    if w[i] == '(': # Handle open parenthesis
        i += 1
        sub_parenthesis = parenthesis_in_stack
        parenthesis_in_stack += 1
        expression = exp()
    else:
        raise ParseError

    if func_name == 'sin':
        expression = math.sin(expression)
    elif func_name == 'cos':
        expression = math.cos(expression)
    elif func_name == 'tan':
        expression = math.tan(expression)
    elif func_name == 'exp':
        expression = math.exp(expression)
    elif func_name == 'sqrt':
        expression = math.sqrt(expression)
    elif func_name == 'abs':
        expression = abs(expression)
    else:
        print('function expected')
        raise ParseError

    return expression
# ---------------------------------------
# Parse a Statement   <statement> → <id> = <exp>
#
def statement():
    global i, err, symbol_table

    object_id = ''
    
    while 1:
        if w[i] == 'pi' or\
            w[i] in '()+-*/' or\
            w[i].isnumeric() or\
            w[i] in symbol_table or\
            w[i] in ['sin', 'cos', 'tan', 'exp', 'sqrt', 'abs']:
            return exp()
        elif w[i] == '=' and object_id != '':
            i += 1
            assign(object_id, exp())
        elif w[i].isdigit() == 0 and w[i] != '$':
            object_id = w[i]
            i += 1
        else:
            break

    return None
#==============================================================
# BACK END PARSER (ACTION RULES)
#==============================================================


def binary_op(op, lhs, rhs):
    if op == '+':
        return lhs + rhs
    elif op == '-':
        return lhs - rhs
    elif op == '*':
        return lhs * rhs
    elif op == '/':
        return lhs / rhs
    else:
        return None


def atomic(x):
    try:
        return float(x)
    except:
        if x in symbol_table:
            return symbol_table.get(x)
        else:
            print('float literal or variable expected')
            raise ParseError


def assign(object_id, value):
    symbol_table[object_id] = value
    return

    
#==============================================================
# User Interface Loop
#==============================================================
w = input('\nEnter expression: ')
while w != '':
    # ------------------------------
    # Split string into token list.
    #
    for c in '()+-*/':
        w = w.replace(c, ' '+c+' ')
    w = w.split()
    w.append('$')  # EOF marker

    print('\nToken Stream:     ', end='')
    for t in w:
        print(t, end='  ')
    print('\n')
    i = 0
    
    # Handle parenthesis with parenthesis_in_stack and sub_parenthesis
    
    # This variable performs similar to stack. If w[i] is '(', then increment
    # parenthesis_in_stack(i.e. add a ( in stack), if w[i] is ')', then
    # decrement parenthesis_in_stack(i.e. remove a ( from stack).
    parenthesis_in_stack = 0

    # Store value before increment or value after decrement.
    sub_parenthesis = 0
    
    try:
        # print('Value:           ', exp())  # call the parser
        value = statement()

        # Check if parentheses are balanced, if yes, call exp(), parse error otherwise
        if parenthesis_in_stack == 0:
            if value is not None:
                print('Value:           ', value)
            else:
                print("Statement successfully assigned")
        else:
            print('unbalanced parenthesis')
            raise ParseError
    except:
        print('parse error')
    print()
    if (w[i] != '$'):
        print('Syntax error:')
    print('read | un-read:   ', end='')
    for c in w[:i]:
        print(c, end='')
    print(' | ', end='')
    for c in w[i:]:
        print(c, end='')
    print()
    print("Symbol table contains " + str(symbol_table))
    w = input('\n\nEnter expression: ')
#print(w[:i], '|', w[i:])
