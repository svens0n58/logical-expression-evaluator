from src.expression import LogicalExpression

expression = "A & !C"

# Create a LogicalExpression object representing the logical expression "A & !C"
logical_expression = LogicalExpression("A & !C")

# Generate a truth table for the expression using the logic '3' (Lukasiewicz 3-valued logic)
logical_expression.truth_table('3')

# Generate a truth table for the expression using the classical logic.
# logical_expression.truth_table()

# Evaluate the expression with specified values for variables A and C
# logical_expression.evaluate_expression(A=1, C=0)
