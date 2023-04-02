def add(a, b):
    return a + b


def substract(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 'Zero Division'


operands = {'+': add,
            '-': substract,
            '*': mul,
            '/': div}


# токенизируем наш инпут
def token(string: str):
    string = string.replace(' ', '')
    llist = []
    llist2 = []
    empty = ''
    n = 0
    for i in string:
        if i in '0123456789.':
            empty += i

        elif i in '+-*/()':
            if empty != '':
                llist.append(float(empty))
            empty = ''
            llist.append(i)

        n += 1

    if empty != '':  # добавляем последнее число в лист
        llist2.append(float(empty))

    almost_final = llist + llist2
    final = almost_final.copy()
    for i in range(len(almost_final)):  # тут смотрим какие из минусов унарные и добавляем их к числам (float)
        if almost_final[i] == '-':
            if ((almost_final[i - 1] == '(') | (i == 0)) & (type(almost_final[i + 1]) == float):
                final[i + 1] = -final[i + 1]
                final.pop(i)

    return final


# reverse polish notation algorithm
def rpna(infix_notation: str):
    infix_notation = token(infix_notation)  # прочитали токен
    priority = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}
    output = []
    stack = []
    for i in infix_notation:

        if type(i) == float:  # Если токен — число, то добавить его в очередь вывода
            output.append(float(i))

        elif i == '(':  # Если токен — открывающая скобка, то положить его в стек
            stack.append(i)

        elif i == ')':  # Если токен — закрывающая скобка, то
            while stack[-1] != '(':  # Пока токен на вершине стека не открывающая скобка
                try:  # Переложить оператор из стека в выходную очередь
                    output.append(stack[-1])
                    stack = stack[:-1]
                except IndexError:  # Если стек закончился до того, как был встречен токен открывающая скобка,
                    # то в выражении пропущена скобка
                    print('2 В выражении пропущена скобка')
            stack.remove('(')

        else:
            if len(stack) > 0:
                if priority[stack[len(stack) - 1]] >= priority[i]:
                    output.append(stack[-1])
                    stack = stack[:-1]
            stack.append(i)

    while len(stack) != 0:
        output.append(stack.pop())

    return output


def counting(formula: str):
    formula = rpna(formula)
    stack = []
    for i in formula:
        if type(i) == float:
            stack.append(float(i))
        else:
            num2 = stack.pop()
            num1 = stack.pop()
            stack.append(operands[i](num1, num2))
    return stack.pop()


assert ((2 + 3.5 - 6) == counting('2+3.5-6'))
assert ((5+((1+2)*4)-3) == counting('5+((1+2)*4)-3'))
assert ((2 + 3.4 - 6 * 3 / (2+1)) == counting('2 + 3.4 - 6 * 3 / (2+1)'))
