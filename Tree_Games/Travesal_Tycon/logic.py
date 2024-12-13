import random

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def generate_random_tree(): 
    total_nodes = 15
    all_numbers = list(range(2, total_nodes + 1))
    random.shuffle(all_numbers)

    nodes = [TreeNode(1)] + [TreeNode(num) for num in all_numbers]
    root = nodes[0]  
 
    root.children = [nodes[1], nodes[2], nodes[3]]
 
    remaining_nodes = nodes[4:]
 
    potential_parents = [root] + root.children
    for node in remaining_nodes:
        parent = random.choice(potential_parents)
        parent.children.append(node)
        potential_parents.append(node)

    return root

def get_tree_layout(root, screen_width, screen_height, min_gap=30):
    
    layout = {}

    def assign_positions(node, depth, x_offset, available_width):
        if not node:
            return
        x_position = x_offset + available_width // 2
        y_position = depth * min_gap
        layout[node.value] = (x_position, y_position)

        num_children = len(node.children)
        if num_children == 0:
            return

        child_width = available_width // num_children
        for i, child in enumerate(node.children):
            assign_positions(child, depth + 1, x_offset + i * child_width, child_width)

    assign_positions(root, 1, 0, screen_width)
    return layout
 
def preorder_traversal(node): 
    if node is None:
        return []
    result = [node.value]
    for child in node.children:
        result.extend(preorder_traversal(child))
    return result

def inorder_traversal(node): 
    if node is None:
        return []
    result = []
    if node.children:
        result.extend(inorder_traversal(node.children[0]))
    result.append(node.value)  
    for child in node.children[1:]:
        result.extend(inorder_traversal(child))
    return result

def postorder_traversal(node): 
    if node is None:
        return []
    result = []
    for child in node.children:  # Visit each child recursively
        result.extend(postorder_traversal(child))
    result.append(node.value)  # Visit root
    return result

def get_traversals(root):
    traversals = {
        'Pre Order': preorder_traversal(root),
        'In Order': inorder_traversal(root),
        'Post Order': postorder_traversal(root)
    }
    return traversals
