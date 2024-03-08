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
        self._exp = _tokenize_expression(expression)
        self._prefix_exp, self._main_connective_position = \
            infix_to_prefix(self.exp)
        self._var = self._extract_variables()
        self._operators_positions = self._get_posiitons_of_operators()
        self._expression_tree = build_tree(self._prefix_exp)[0]
        self._operators_evaluations = [[] if i in self._operators_positions
                                       else ' ' for i in range(len(self.exp))]

    @property
    def var(self):
        return self._var

    @property
    def operators_positions(self):
        return self._operators_positions

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, expression):
        self.__init__(expression)

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
            if not self.operators_positions:
                self.operators_evaluations[root.position] = values[root.data]
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

        elif root.data == "->":
            self.operators_evaluations[root.position] = \
                min(1, 1 - left_side + right_side)
            return min(1, 1 - left_side + right_side)

        elif root.data == "<->":
            self.operators_evaluations[root.position] = \
                1 - abs(left_side - right_side)
            return 1 - abs(left_side - right_side)

    def _create_dict(self, comb):
        values = {}
        for i, c in enumerate(comb):
            values[self.var[i]] = c
        return values

    def _print_first_line(self):
        length_expression = 3 * len(self.var) + 3 * len(self.exp) + 7 + \
            sum([token.additional_space for token in self.exp])
        if self._main_connective_position == 0:
            length_expression -= 3
        print(*self.var, sep='  ', end='  /  ')
        expression = [token.value for token in self.exp]
        expression_left = expression[:self._main_connective_position]
        expression_right = expression[self._main_connective_position+1:]
        if expression_left:
            print(*expression_left, sep='  ', end='  /  ')
        print(expression[self._main_connective_position], end='  /  ')
        if expression_right:
            print(*expression_right, sep='  ')
        else:
            print("")
        print("-" * length_expression)

    def _print_evaluation_line(self, values):
        print(*values.values(), sep='  ', end='  /  ')
        tree = self.expression_tree
        self._evaluate_tree(tree, values)
        evaluations_left = \
            self.operators_evaluations[:self._main_connective_position]
        evaluations_right = \
            self.operators_evaluations[self._main_connective_position+1:]
        if evaluations_left:
            print(*evaluations_left, sep='  ', end='  /  ')
        print(self.operators_evaluations[self._main_connective_position],
              end='  /  ')
        if evaluations_right:
            print(*evaluations_right, sep='  ')
        else:
            print("")

    def truth_table(self):
        self._print_first_line()
        combinations = self._all_combinations(len(self.var))

        for comb in combinations:
            values = self._create_dict(comb)
            self._print_evaluation_line(values)

    def _check_user_values(self, values):
        for key, value in values.items():
            if key not in self.var:
                raise ValueError(f"Variable {key} was specified but does not"
                                 f" exist in the expression. This is the list"
                                 f" of variables in the expression {self.var}")

            if not isinstance(value, float) and not isinstance(value, int):
                raise TypeError(f"Value specified for variable {key} is not of"
                                f" int or float type, it is of {type(value)}")
            if value < 0 or value > 1:
                raise ValueError(f"Value specified for variable {key} is "
                                 f" {value} which is not in the range [0, 1].")

    def evaluate_expression(self, **values):
        self._check_user_values(values)

        self._print_first_line()

        self._print_evaluation_line(values)
