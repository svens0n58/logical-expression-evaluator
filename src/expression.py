from src.scanner import _tokenize_expression, TokenType, infix_to_prefix
from src.expression_tree import build_tree
from itertools import product

'''
To do list:
1. check if validating is correct (espacially with parenthesis) (not correct
when & !C A ! B) [DONE]
2. infix to expression tree (maybe a lot of subtrees). [DONE]
3. implement position of operators and the main_connective [DONE]
'''


class LogicalExpression():
    def __init__(self, expression: str):
        self.exp = _tokenize_expression(expression)
        self._prefix_exp, self._main_connective_position = \
            infix_to_prefix(self.exp)
        self._var = self._extract_variables()
        self._operators_positions = self._get_posiitons_of_operators()
        self._expression_tree = build_tree(self._prefix_exp)[0]
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
    def expression_tree(self):
        return self._expression_tree

    @property
    def operators_evaluations(self):
        return self._operators_evaluations

    def _extract_variables(self):
        variables = set()
        for token in self.exp:
            if token.type == TokenType.VARIABLE:
                variables.add(token.value)

        return sorted(variables)

    def _get_posiitons_of_operators(self):
        positions = []
        for i, token in enumerate(self.exp):
            if token.type == TokenType.OPERATOR or \
                    token.type == TokenType.NEGATION:
                positions.append(i)
        return positions

    def _all_combinations(self, n):
        return list(product([1, 0], repeat=n))

    def _evaluate_tree(self, root, values):
        if root is None:
            return 0

        if root.left is None and root.right is None:
            return values[root.data]

        left_side = self._evaluate_tree(root.left, values)

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

        elif root.type == TokenType.NEGATION:
            self.operators_evaluations[root.position] = 1 - left_side
            return 1 - left_side

    def _create_dict(self, comb):
        values = {}
        for i, c in enumerate(comb):
            values[self.var[i]] = c
        return values

    def truth_table(self):
        print(*self.var, sep='  ', end='  /  ')
        expression = [token.value for token in self.exp]
        expression_left = expression[:self._main_connective_position]
        expression_right = expression[self._main_connective_position+1:]

        print(*expression_left, sep='  ', end='  /  ')
        print(expression[self._main_connective_position], end='  /  ')
        print(*expression_right, sep='  ')
        print("-" * (3 * len(self.var) + 3 * len(self.exp) + 7))

        tree = self._expression_tree
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
