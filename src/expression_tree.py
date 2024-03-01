from src.scanner import TokenType


class TreeNode():
    def __init__(self, data):
        self.data = data.value
        self.type = data.type
        self.position = data.position
        self.left = None
        self.right = None


def build_tree(s):
    if s[0].type == TokenType.VARIABLE:
        return TreeNode(s[0]), s[1:]
    else:
        if s[0].type == TokenType.NEGATION:
            p = TreeNode(s[0])
            p.left, q = build_tree(s[1:])
            return p, q
        else:
            p = TreeNode(s[0])
            # Build the left sub-tree
            p.left, q = build_tree(s[1:])
            # Build the right sub-tree
            p.right, q = build_tree(q)
            return p, q
