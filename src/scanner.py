from enum import Enum

OPERATORS = ['&', '|']
START_OPERATORS = ['-', '<']
NEGATIONS = ['!', '~']
SYMBOLS = ['(', ')']


class TokenType(Enum):
    OPERATOR = 1
    SYMBOL = 2
    VARIABLE = 3
    NEGATION = 4


class Token():
    def __init__(self, value, type, position):
        self._value = value
        self._type = type
        self.position = position

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type


def _match_operator(expression, position):
    if len(expression) - 1 >= position + 1 and expression[position] == '-' \
            and expression[position+1] == '>':
        return "->", position + 1
    elif len(expression) - 1 >= position + 2 and expression[position] == '<' \
            and expression[position+1] == '-' and \
            expression[position+2] == '>':
        return "<->", position + 2
    else:
        raise ValueError("Provided expression is not valid.")


def _generate_token(expression, position, i):
    if expression[position].isalpha():
        new_position = position
        new_token = Token(expression[position], TokenType.VARIABLE, i)
    elif expression[position] in OPERATORS:
        new_position = position
        new_token = Token(expression[position], TokenType.OPERATOR, i)
    elif expression[position] in START_OPERATORS:
        operator, new_position = _match_operator(expression, position)
        new_token = Token(operator, TokenType.OPERATOR, i)
    elif expression[position] in NEGATIONS:
        new_position = position
        new_token = Token(expression[position], TokenType.NEGATION, i)
    elif expression[position] in SYMBOLS:
        new_position = position
        new_token = Token(expression[position], TokenType.SYMBOL, i)
    else:
        raise ValueError("Provided expression is not valid.")
    return new_token, new_position


def _tokenize_expression(expression):
    position = 0
    i = 0
    tokens = []
    while position < len(expression):
        if expression[position].isspace():
            position += 1
        else:
            new_token, position = _generate_token(expression, position, i)
            i += 1
            tokens.append(new_token)
            position += 1
    if _check_validity_token_list(tokens):
        return tokens
    else:
        raise SyntaxError("Provided expression is not valid.")


def _check_validity_token_list(token_list):
    tokenized_expression = []
    for token in token_list:
        if token.type == TokenType.VARIABLE:
            tokenized_expression.append("True")
        elif token.type == TokenType.NEGATION:
            tokenized_expression.append("~")
        elif token.type == TokenType.SYMBOL:
            tokenized_expression.append(token.value)
        else:
            tokenized_expression.append('&')
    tokenized_expression = ' '.join(str(t) for t in tokenized_expression)

    try:
        eval(tokenized_expression)
        return True
    except SyntaxError:
        return False


def prec(token):
    if token.type == TokenType.NEGATION:
        return 2
    if token.type == TokenType.OPERATOR:
        return 1
    else:
        return -1


def infix_to_prefix(s):
    result = []
    stack = []

    for i in range(len(s)):
        if s[i].type == TokenType.VARIABLE:
            result.append((s[i], i))
        elif s[i].value == '(':
            stack.append((s[i], i))
        elif s[i].value == ')':
            while len(stack) > 0 and stack[-1][0].value != '(':
                result.append(stack.pop())
            stack.pop()
        else:
            while len(stack) > 0 and prec(s[i]) < prec(stack[-1][0]):
                result.append(stack.pop())
            stack.append((s[i], i))
    while len(stack) > 0:
        result.append(stack.pop())

    main_connective_position = result[-1][1]
    return [x[0] for x in result[::-1]], main_connective_position
