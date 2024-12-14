import math

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class BinarySearchTree:
    def __init__(self):
        self.extra_nodes_used = 0  # Track how many extra nodes are used

    def insert(self, root, key):
        if not root:
            return Node(key)

        # Perform standard BST insertion
        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)

        # Update height of the ancestor node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Balance the tree if needed
        balance = self.get_balance(root)
        if balance > 1:
            if key < root.left.key:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        if balance < -1:
            if key > root.right.key:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)

        return root
    def sorted_array_to_bst(self, arr, start, end):
        """Helper function to construct a balanced BST from a sorted array."""
        if start > end:
            return None
        mid = (start + end) // 2
        node = Node(arr[mid])
        node.left = self.sorted_array_to_bst(arr, start, mid - 1)
        node.right = self.sorted_array_to_bst(arr, mid + 1, end)
        return node

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right)
    def get_root(self, keys):
        """Construct a balanced BST from the given keys."""
        keys.sort()  # Sort the keys to ensure the BST is balanced
        return self.sorted_array_to_bst(keys, 0, len(keys) - 1)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def check_win_condition(self, root, initial_keys, extra_keys):
        """Check if the final tree height matches the minimum height."""
        total_nodes = len(initial_keys) + len(extra_keys)
        hypothetical_height = self.calculate_minimum_height(total_nodes)
        actual_height = self.get_height(root)

        return actual_height == hypothetical_height

    def calculate_minimum_height(self, n):
        """Calculate the minimum height for a balanced tree with n nodes."""
        return math.ceil(math.log2(n + 1)) - 1

    def isBalanced(self, root):
        """Check if the tree is balanced."""
        if not root:
            return True

        left_height = self.get_height(root.left)
        right_height = self.get_height(root.right)

        if abs(left_height - right_height) > 1:
            return False

        # Recursively check left and right subtrees
        return self.isBalanced(root.left) and self.isBalanced(root.right)
    def isBST(self, root):
        def in_order_traversal(node, prev=[None]):
            if not node:
                return True
            if not in_order_traversal(node.left, prev):
                return False
            if prev[0] is not None and node.key <= prev[0].key:
                return False
            prev[0] = node
            return in_order_traversal(node.right, prev)
        return in_order_traversal(root)

