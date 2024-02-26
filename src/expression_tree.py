class Node():
    def __init__(self, data):
        self.data = data.token
        self.type = data.type
        self.position = data.position
        self.left = None
        self.right = None


def build(s):
    # If the character is an operand
    if (s == ''):
        return ''

        # If the character is an operand
    if s[0].type == "variable":
        return Node(s[0]), s[1:]
    else:
        if s[0].token == '!':
            p = Node(s[0])
            p.left, q = build(s[1:])
            return p, q
        else:
            p = Node(s[0])
            # Build the left sub-tree
            p.left, q = build(s[1:])
            # Build the right sub-tree
            p.right, q = build(q)
            return p, q


def prec(token):
    if token.token == '!':
        return 2
    if token.type == "operator":
        return 1
    else:
        return -1


def infix_to_prefix(s):
    result = []
    stack = []

    for i in range(len(s)):
        if s[i].type == "variable":
            result.append((s[i], i))
        elif s[i].token == '(':
            stack.append((s[i], i))
        elif s[i].token == ')':
            while len(stack) > 0 and stack[-1][0].token != '(':
                result.append(stack.pop())
            stack.pop()
        else:
            while len(stack) > 0 and prec(s[i]) < prec(stack[-1][0]):
                result.append(stack.pop())
            stack.append((s[i], i))
    while len(stack) > 0:
        result.append(stack.pop())

    main_connective_position = result[-1][1]
    return [x[0] for x in result[::-1]], main_connective_position
