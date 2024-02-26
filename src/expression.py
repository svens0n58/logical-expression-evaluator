from expression_tree import infix_to_prefix, build
from itertools import product

'''
To do list:
1. check if validating is correct (espacially with parenthesis) (not correct
when & !C A ! B)
2. infix to expression tree (maybe a lot of subtrees). [DONE]
3. implement position of operators and the main_connective [DONE]
'''


class Token():
    def __init__(self, token, type, position):
        self._token = token
        self._type = type
        self.position = position

    @property
    def token(self):
        return self._token

    @property
    def type(self):
        return self._type


class LogicalExpression():
    def __init__(self, expression: str):
        self._operators = ['|', '&', '!']
        self._symbols = ['(', ')']
        self.exp = self._tokenize_expression(expression)
        self._prefix_exp, self._main_connective_position = \
            infix_to_prefix(self.exp)
        self._var = self._extract_variables()
        self._expression_tree = build(self._prefix_exp)
        self._operators_positions = self._get_posiitons_of_operators()
        self._operators_evaluations = [[] if i in self._operators_positions
                                       else ' ' for i in range(len(self.exp))]

    @property
    def operators(self):
        return self._operators

    @property
    def symbols(self):
        return self._symbols

    @property
    def var(self):
        return self._var

    @property
    def operators_evaluations(self):
        return self._operators_evaluations

    def _extract_variables(self):
        variables = set()
        for token in self.exp:
            if token.type == "variable":
                variables.add(token.token)

        return sorted(variables)

    def _get_posiitons_of_operators(self):
        positions = []
        for i, token in enumerate(self.exp):
            if token.type == "operator":
                positions.append(i)
        return positions

    def _all_combinations(self, n):
        return list(product([1, 0], repeat=n))

    def _check_validity_token_list(self, token_list):
        position = 0
        parenthesis = 0
        if len(token_list) == 0:
            return False
        if (token_list[0].type == "operator" and token_list[0].token != '!') \
                or token_list[-1].type == "operator":
            return False
        while position < len(token_list) - 1:
            if token_list[position].type == "variable" and \
                    token_list[position+1].type == "variable":
                return False
            if token_list[position].type == "operator" and \
                    (token_list[position+1].type == "operator" and
                     token_list[position+1].token != '!'):
                return False
            if token_list[position].token == '(':
                parenthesis += 1
            if token_list[position].token == ')':
                parenthesis -= 1
                if parenthesis < 0:
                    return False
            position += 1
        if token_list[position].token == '(':
            parenthesis += 1
        if token_list[position].token == ')':
            parenthesis -= 1
            if parenthesis < 0:
                return False
        if parenthesis != 0:
            return False

        return True

    def _generate_token(self, token, position):
        if token.isalpha():
            new_token = Token(token, "variable", position)
        elif token in self.operators:
            new_token = Token(token, "operator", position)
        elif token in self.symbols:
            new_token = Token(token, "symbol", position)
        else:
            raise ValueError("Provided expression is not valid.")

        return new_token

    def _tokenize_expression(self, expression):
        position = 0
        i = 0
        tokens = []
        while position < len(expression):
            if expression[position].isspace():
                position += 1
            else:
                new_token = self._generate_token(expression[position], i)
                i += 1
                tokens.append(new_token)
                position += 1
        if self._check_validity_token_list(tokens):
            return tokens
        else:
            raise ValueError("Provided expression is not valid.")

    def _evaluate_tree(self, root, values):
        if root is None:
            return 0

            # leaf node
        if root.left is None and root.right is None:
            return values[root.data]

        # evaluate left tree
        left_side = self._evaluate_tree(root.left, values)

        # evaluate right tree
        right_side = self._evaluate_tree(root.right, values)

        # check which operation to apply
        if root.data == '&':
            self.operators_evaluations[root.position] = min(left_side,
                                                            right_side)
            return min(left_side, right_side)

        elif root.data == '|':
            self.operators_evaluations[root.position] = max(left_side,
                                                            right_side)
            return max(left_side, right_side)

        elif root.data == '!':
            self.operators_evaluations[root.position] = 1 - left_side
            return 1 - left_side

    def _create_dict(self, comb):
        values = {}
        for i, c in enumerate(comb):
            values[self.var[i]] = c
        return values

    def truth_table(self):
        print(*self.var, sep='  ', end='  /  ')
        expression = [token.token for token in self.exp]
        expression_left = expression[:self._main_connective_position]
        expression_right = expression[self._main_connective_position+1:]

        print(*expression_left, sep='  ', end='  /  ')
        print(expression[self._main_connective_position], end='  /  ')
        print(*expression_right, sep='  ')
        print("-" * (3 * len(self.var) + 3 * len(self.exp) + 7))
        tree = build(lol._prefix_exp)[0]
        combinations = self._all_combinations(len(self.var))

        for comb in combinations:
            print(*comb, sep='  ', end='  /  ')
            values = self._create_dict(comb)
            self._evaluate_tree(tree, values)
            # print(*self.operators_evaluations)
            evaluations_left = \
                self.operators_evaluations[:self._main_connective_position]
            evaluations_right = \
                self.operators_evaluations[self._main_connective_position+1:]
            print(*evaluations_left, sep='  ', end='  /  ')
            print(self.operators_evaluations[self._main_connective_position],
                  end='  /  ')
            print(*evaluations_right, sep='  ')


lol = LogicalExpression("A & !B")
print([x.token for x in lol.exp])
print(len(lol.exp))
print([x.position for x in lol.exp])
print(lol._var)
print(lol._operators_positions)
print([x.token for x in lol._prefix_exp])
print(lol._main_connective_position)
print(len(lol.exp))
lol.truth_table()
