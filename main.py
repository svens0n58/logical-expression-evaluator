from src.expression import LogicalExpression

expression = LogicalExpression("A <-> B")
expression.truth_table()
expression.evaluate_expression(A=1, B=0)
