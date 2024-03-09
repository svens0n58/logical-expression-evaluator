from src.expression import LogicalExpression

expression = LogicalExpression("A & !C")

expression.truth_table('3')

# expression.evaluate_expression(A=1, B=0, C=0)
