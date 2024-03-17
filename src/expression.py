# 2024 Sven van Loon

from src.scanner import _tokenize_expression, TokenType, infix_to_prefix, Token
from src.expression_tree import build_tree, TreeNode
from itertools import product
from typing import List


class LogicalExpression():
    def __init__(self, expression: str) -> None:
        self._exp = _tokenize_expression(expression)
        self._prefix_exp, self._main_connective_position = \
            infix_to_prefix(self.exp)
        self._var = self._extract_variables()
        self._operators_positions = self._get_positions_of_operators()
        self._expression_tree = build_tree(self._prefix_exp)[0]
        self._evaluations = [0 if i in self._operators_positions else ' '
                             for i in range(len(self.exp))]

    @property
    def var(self) -> List[str]:
        """
        Getter method for the '_var' property.

        Returns:
            List[str]: A list containing variables specified in the expression.

        """
        return self._var

    @property
    def operators_positions(self) -> List[int]:
        """
        Getter method for the '_operators_positions' property.

        Returns:
            List[int]: A list containing the positions of the operators in the
            expression.

        """
        return self._operators_positions

    @property
    def exp(self) -> List[Token]:
        """
        Getter method for the '_exp' property.

        Returns:
            List[Token]: A list containing tokenized elements of the
            expression.

        """
        return self._exp

    @exp.setter
    def exp(self, expression: str) -> None:
        """
        Setter method for the 'exp' property.

        Args:
            expression (str): The new expression to be assigned.

        """
        self.__init__(expression)

    @property
    def expression_tree(self) -> TreeNode:
        """
        Getter method for the '_expression_tree' property.

        Returns:
            TreeNode: A root of the expression tree constructed from the
            expression.

        """
        return self._expression_tree

    @property
    def evaluations(self) -> List[str | int]:
        """
        Getter method for the '_evaluations' property.

        Returns:
            List[str | int]: A list containing evaluations of each element in
            the tokenized expression.

        """
        return self._evaluations

    def _extract_variables(self) -> List[str]:
        """
        Extracts variables from the expression.

        Returns:
            List[str]: A sorted list of unique variables found in the
            expression.

        """
        variables = set()
        for token in self.exp:
            if token.type == TokenType.VARIABLE:
                variables.add(token.value)

        return sorted(variables)

    def _get_positions_of_operators(self) -> List[int]:
        """
        Extracts the index positions of operators in the expression.

        Returns:
            List[int]: A list of index positions of operators in the
            expression.

        """
        positions = []
        for i, token in enumerate(self.exp):
            if token.type == TokenType.OPERATOR or \
                    token.type == TokenType.NEGATION:
                positions.append(i)
        return positions

    def _all_combinations(self, n, logic) -> List[List[int]]:
        """
        Generate all possible combinations of truth values.

        Args:
            n (int): The number of variables.
            logic (str or None): The logic type, can be None (propositional
            logic) or '3' (Lukasiewicz 3 valued logic).

        Returns:
            List[List[int]]: A list containing all possible combinations of
            truth values.

        """
        if logic is None:
            return list(product([1, 0], repeat=n))
        elif logic == '3':
            return list(product([1, 0.5, 0], repeat=n))

    def _evaluate_tree(self, root: TreeNode, values: dict) -> int:
        """
        Recursively evaluates the truth value at all positions of a logical
        expression tree and stores them in 'self._evaluations' attribute.

        Args:
            root (TreeNode): The root node of the logical expression tree.
            values (dict): A dictionary containing truth values for variables.

        Returns:
            int: The evaluated truth value of the expression
            represented by the tree.

        """
        if root is None:
            return 0

        if root.left is None and root.right is None:
            if not self.operators_positions:
                self.evaluations[root.position] = values[root.data]
            return values[root.data]

        left_side = self._evaluate_tree(root.left, values)

        right_side = self._evaluate_tree(root.right, values)

        # check which operation to apply
        if root.data == '&':
            self.evaluations[root.position] = min(left_side, right_side)
            if self.evaluations[root.position] == 0.5:
                self.evaluations[root.position] = 'i'
            return min(left_side, right_side)

        elif root.data == '|':
            self.evaluations[root.position] = max(left_side, right_side)
            if self.evaluations[root.position] == 0.5:
                self.evaluations[root.position] = 'i'
            return max(left_side, right_side)

        elif root.type == TokenType.NEGATION:
            self.evaluations[root.position] = 1 - left_side
            if self.evaluations[root.position] == 0.5:
                self.evaluations[root.position] = 'i'
            return 1 - left_side

        elif root.data == "->":
            self.evaluations[root.position] = \
                min(1, 1 - left_side + right_side)
            if self.evaluations[root.position] == 0.5:
                self.evaluations[root.position] = 'i'
            return min(1, 1 - left_side + right_side)

        elif root.data == "<->":
            self.evaluations[root.position] = \
                1 - abs(left_side - right_side)
            if self.evaluations[root.position] == 0.5:
                self.evaluations[root.position] = 'i'
            return 1 - abs(left_side - right_side)

    def _create_dict(self, comb: List) -> dict:
        """
        Creates a dictionary mapping variable names to truth values.

        Args:
            comb (iterable): The combination of truth values for variables.

        Returns:
            dict: A dictionary where variable names are keys and their
            corresponding truth values are values.

        """
        values = {}
        for i, c in enumerate(comb):
            values[self.var[i]] = c
        return values

    def _print_first_line(self) -> None:
        """
        Print the first line of the expression representation, separating
        variables and expression with '/'. Seperates the main connective
        operator with '/' from both sides.

        The length of the expression is calculated based on the length of
        variables, expression parts, and any additional spaces specified by
        tokens. If the main connective is at the beginning of the expression,
        the length is adjusted accordingly.

        Returns:
            None: This function does not return anything. It prints the
            formatted expression to the console.
        """
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

    def _print_evaluation_line(self, values: dict) -> None:
        """
        Print the evaluation line of the expression, showing the values of
        variables and the evaluation corresponding to each operator in
        expression.

        Args:
            values (dict): A dictionary containing variable names and their
            corresponding values.

        Returns:
            None: This function does not return anything. It prints the
            formatted evaluation line to the console.
        """
        correct_format_values = ['i' if i == 0.5 else i for i in
                                 values.values()]
        print(*correct_format_values, sep='  ', end='  /  ')
        tree = self.expression_tree
        self._evaluate_tree(tree, values)
        evaluations_left = \
            self.evaluations[:self._main_connective_position]
        evaluations_right = \
            self.evaluations[self._main_connective_position+1:]
        if evaluations_left:
            print(*evaluations_left, sep='  ', end='  /  ')
        print(self.evaluations[self._main_connective_position],
              end='  /  ')
        if evaluations_right:
            print(*evaluations_right, sep='  ')
        else:
            print("")

    def truth_table(self, logic: str | None = None) -> None:
        """
        Generate and print the truth table for the logical expression.

        This function prints the first line of the expression representation,
        followed by the evaluation lines representing different combinations
        of truth values for the variables.

        Args:
            logic (str or None): Specifies the logic to be used. If None,
            defaults to classical logic, if '3' Lukasiewicz logic.

        Returns:
            None: This function does not return anything. It prints the truth
            table to the console.
        """
        self._print_first_line()
        combinations = self._all_combinations(len(self.var), logic)

        for comb in combinations:
            values = self._create_dict(comb)
            self._print_evaluation_line(values)

    def _check_user_values(self, values: dict) -> None:
        """
        Check if the user-specified values for variables are valid.

        This function iterates through the provided dictionary of
        variable-value pairs and checks if each variable exists in the
        expression, if the corresponding value is of type int or float, and if
        the value is within the valid range [0, 1].

        Args:
            values (dict): A dictionary containing variable names and their
            corresponding values.

        Raises:
            ValueError: If a variable specified by the user does not exist in
            the expression, or if the value specified for a variable is
            outside the valid range [0, 1].
            TypeError: If the value specified for a variable is not of type
            int or float.

        Returns:
            None: This function does not return anything. It raises an
            exception if invalid values are found.
        """
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
        """
        Evaluate the logical expression with user-specified values for
        variables.

        This function evaluates the logical expression with the provided
        values for variables. It first checks if the user-specified values are
        valid using the _check_user_values method, then prints the first line
        of the expression representation, followed by the evaluation line
        showing the computed values of variables and intermediate evaluation
        results of the expression.

        Args:
            **values: Keyword arguments representing variable names and their
            corresponding values.

        Returns:
            None: This function does not return anything. It prints the
            evaluated expression to the console.

        Raises:
            ValueError: If a variable specified by the user does not exist in
                the expression, or if the value specified for a variable is
                outside the valid range [0, 1].
            TypeError: If the value specified for a variable is not of type
                int or float.
        """
        self._check_user_values(values)

        self._print_first_line()

        self._print_evaluation_line(values)
