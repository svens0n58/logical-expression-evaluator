from src.scanner import TokenType


class TreeNode():
    def __init__(self, data):
        self.data = data.value
        self.type = data.type
        self.position = data.position
        self.left = None
        self.right = None


def build_tree(s):
    """
    Build a binary tree from a prefix expression.

    This function constructs a binary tree representing a logical expression
    from a prefix expression represented as a list of tokens.

    Args:
        s (list): A list of tokens representing the prefix expression.

    Returns:
        tuple: A tuple containing the root node of the constructed tree
            and the remaining tokens after constructing the tree.
    """
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
            p.right, q = build_tree(s[1:])
            # Build the right sub-tree
            p.left, q = build_tree(q)
            return p, q
