# 2024 Sven van Loon

from enum import Enum
from typing import Tuple, List

OPERATORS = ['&', '|']
START_OPERATORS = ['-', '<']
NEGATIONS = ['!', '~']
SYMBOLS = ['(', ')']


class TokenType(Enum):
    """
        Tokens can be of four types:
        operators, symvols, variables, and negations.
    """
    OPERATOR = 1
    SYMBOL = 2
    VARIABLE = 3
    NEGATION = 4


class Token():
    def __init__(self, value, type, position, additional_space=0):
        self._value = value
        self._type = type
        self._position = position
        self._additional_space = additional_space

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @property
    def position(self):
        return self._position

    @property
    def additional_space(self):
        return self._additional_space


def _match_operator(expression: str, position: int) -> Tuple[str, int, int]:
    """
    Match logical operators in the expression starting from the specified
    position.

    This function examines the expression starting from the specified position
    to identify logical operators ('->' for implication and '<->' for
    biconditional). If a match is found, the operator string, its position,
    and the number of characters consumed are returned.

    Args:
        expression (str): The logical expression to match operators within.
        position (int): The starting position to begin matching within the
        expression.

    Returns:
        tuple: A tuple containing the matched operator string, its position,
        and the number of characters consumed.

    Raises:
        ValueError: If the provided expression does not contain a valid
        logical operator starting from the specified position.

    Example:
        >>> _match_operator("p -> q", 2)
        ('->', 3, 1)
        >>> _match_operator("p <-> q", 2)
        ('<->', 4, 2)
    """
    if len(expression) - 1 >= position + 1 and expression[position] == '-' \
            and expression[position+1] == '>':
        return "->", position + 1, 1
    elif len(expression) - 1 >= position + 2 and expression[position] == '<' \
            and expression[position+1] == '-' and \
            expression[position+2] == '>':
        return "<->", position + 2, 2
    else:
        raise ValueError("Provided expression is not valid.")


def _generate_token(expression: str, position: int, i: int) -> Tuple[Token,
                                                                     int] | \
                                                                        None:
    """
    Generate a token from the character at the specified position in the
    expression.

    This function analyzes the character at the given position in the
    expression and generates a token based on its type (variable, operator,
    negation, symbol). It also handles cases where the character represents
    special operators (e.g., '->' for implication, '<->' for biconditional).

    Args:
        expression (str): The logical expression from which to generate tokens.
        position (int): The position in the expression to analyze.
        i (int): The index of the token.

    Returns:
        tuple: A tuple containing the generated token and the new position in
        the expression.

    Raises:
        ValueError: If the provided expression does not contain a valid
        character at the specified position.

    Example:
        >>> _generate_token("p -> q", 2, 0)
        (Token(value='->', token_type=<TokenType.OPERATOR: 1>, index=0,
        additional_space=1), 4)
    """
    if expression[position].isalpha():
        new_position = position
        new_token = Token(expression[position], TokenType.VARIABLE, i)
    elif expression[position] in OPERATORS:
        new_position = position
        new_token = Token(expression[position], TokenType.OPERATOR, i)
    elif expression[position] in START_OPERATORS:
        operator, new_position, additional_space = \
            _match_operator(expression, position)
        new_token = Token(operator, TokenType.OPERATOR, i, additional_space)
    elif expression[position] in NEGATIONS:
        new_position = position
        new_token = Token(expression[position], TokenType.NEGATION, i)
    elif expression[position] in SYMBOLS:
        new_position = position
        new_token = Token(expression[position], TokenType.SYMBOL, i)
    else:
        raise ValueError("Provided expression is not valid.")
    return new_token, new_position


def _tokenize_expression(expression: str) -> List[Token]:
    """
    Tokenize the logical expression.

    This function breaks down the provided logical expression into individual
    tokens representing variables, operators, negations, or symbols. It uses
    the _generate_token function to generate tokens from characters in the
    expression.

    Args:
        expression (str): The logical expression to tokenize.

    Returns:
        list: A list of tokens generated from the expression.

    Raises:
        SyntaxError: If the provided expression contains invalid tokens or
        syntax.

    Example:
        >>> _tokenize_expression("p -> q")
        [Token(value='p', token_type=<TokenType.VARIABLE: 0>, index=0),
         Token(value='->', token_type=<TokenType.OPERATOR: 1>, index=1,
         additional_space=1),
         Token(value='q', token_type=<TokenType.VARIABLE: 0>, index=2)]
    """
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


def _check_validity_token_list(token_list: List[Token]) -> bool:
    """
    Check the validity of the token list representing a logical expression.

    This function constructs a tokenized expression from the list of tokens
    provided. It then attempts to evaluate the tokenized expression using
    Python's eval function. If the expression is syntactically valid, it
    returns True; otherwise, it returns False.

    Args:
        token_list (list): A list of Token objects representing the logical
        expression.

    Returns:
        bool: True if the token list represents a valid logical expression,
        False otherwise.
    """
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


def infix_to_prefix(s: List) -> Tuple[List[Token], int]:
    """
    Convert an infix expression to a prefix expression.

    This function takes an infix expression represented as a list of tokens
    and converts it into a prefix expression.

    Args:
        s (list): A list of tokens representing the infix expression.

    Returns:
        tuple: A tuple containing the prefix expression as a list of tokens
            and the position of the main connective in the original expression.

    """

    def prec(token: Token) -> int:
        """
        Determine the precedence of a token.

        This function assigns a precedence value to a token based on its type.
        Higher precedence values indicate higher priority in the order of
        operations.

        Args:
            token (Token): The token for which to determine precedence.

        Returns:
            int: The precedence value of the token.
        """

        if token.type == TokenType.NEGATION:
            return 2
        if token.type == TokenType.OPERATOR:
            return 1
        else:
            return -1
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
