from src.expression import LogicalExpression


# Create a LogicalExpression object representing the logical expression "A & !C"
expression = LogicalExpression("A & !C")

# Generate a truth table for the expression using the logic '3' (Lukasiewicz 3-valued logic)
expression.truth_table('3')

# Generate a truth table for the expression using the classical logic.
# expression.truth_table()

# Evaluate the expression with specified values for variables A and C
expression.evaluate_expression(A=1, C=0)
