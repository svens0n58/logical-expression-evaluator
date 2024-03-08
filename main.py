from src.expression import LogicalExpression

expression = LogicalExpression("A & B | !C")

expression.evaluate_expression(A=0, B=0, C=0)
