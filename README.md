# logical-expression-evaluator
Here I will code a logical expression evaluator, it will be able to make truth tables and evaluate them.

# Truth Table Generator and Evaluator for Logical Expressions

## Overview
This Python script generates truth tables for logical expressions and it can also evaluate it with user specified truth values. It allows users to input a logical expression directly in the code and prints out all possible combinations of truth values for the variables in the expression, along with the resulting truth value of the expression for each combination.

## Usage

To use the truth table generator and evaluator:

1. Install Python on your system if you haven't already.
2. Clone or download this repository to your local machine.
3. Navigate to the directory containing the `main.py` script.
4. Open the script in a text editor.
5. Locate the section of the code where the expression is defined.
6. Change the expression to the desired logical expression. For example:

```python
expression = "A & B"
```

7. Save the changes to the script.
8. Run the script with Python. Example:

```bash
python3 main.py
```

## Supported Operators

The script supports the following logical operators:

* '&': Logical AND
* '|': Logical OR
* '!': Logical NOT
* '~': Logical NOT
* '->': Logical CONDITIONAL
* '<->: Logical BICONDITIONAL

## Supported logic

The script supports the following logics:

* Propositional Logic
* Lukasiewicz 3 valued Logic