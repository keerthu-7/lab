
class Node:
    def __init__(self, name, node_type="OR", cost=0):
        self.name = name
        self.type = node_type  # "OR" or "AND"
        self.cost = cost
        self.children = []  # [(child_node(s), edge_cost)]
        self.solved = False

    def add_child(self, child, cost=0):
        self.children.append((child, cost))


def ao_star(node):
    # Base case: leaf node
    if not node.children:
        return node.cost

    if node.type == "OR":
        node.cost = min(
            ao_star(child) + edge_cost
            if isinstance(child, Node)
            else sum(ao_star(c) for c in child) + edge_cost
            for child, edge_cost in node.children
        )
    else:  # AND node
        node.cost = sum(
            ao_star(child) + edge_cost
            if isinstance(child, Node)
            else sum(ao_star(c) for c in child) + edge_cost
            for child, edge_cost in node.children
        )

    node.solved = True
    return node.cost



nodes = {}
n = int(input("Enter number of nodes: "))

# Create nodes
for _ in range(n):
    name = input("Enter node name: ").strip()
    node_type = input("Enter type (OR/AND): ").upper()
    cost = int(input(f"Enter heuristic cost for {name}: "))
    nodes[name] = Node(name, node_type, cost)

# Add edges
e = int(input("Enter number of edges: "))
for _ in range(e):
    line = input("Enter edge (parent children cost): ")
    # Example: A B 1   OR   A (C,D) 2
    parts = line.split()
    u, v, c = parts[0], parts[1], int(parts[2])
    if v.startswith("(") and v.endswith(")"):
        children_names = v.strip("()").split(",")
        children = [nodes[name.strip()] for name in children_names]
        nodes[u].add_child(children, c)  # AND-group
    else:
        nodes[u].add_child(nodes[v], c)  # single child

# Root node
root_name = input("Enter root node: ").strip()
root = nodes[root_name]

# Run AO*
print("Solution cost from root:", ao_star(root)) 

"""
#second ao_star code

class Node:
    def __init__(self, name, node_type="OR", heuristic=0):
        self.name = name
        self.type = node_type.upper()  # "OR" or "AND"
        self.h = heuristic             # heuristic (estimated cost)
        self.children = []             # [(child_node(s), edge_cost)]
        self.solved = False
        self.cost = heuristic           # current best cost

    def add_child(self, child, cost=0):
        self.children.append((child, cost))


def compute_cost(node, cost_table):
    
    if not node.children:
        return node.h

    if node.type == "OR":
        # Choose minimum among children or AND groups
        return min(
            (
                sum(cost_table[c.name] for c in child) + edge_cost
                if isinstance(child, list)
                else cost_table[child.name] + edge_cost
            )
            for child, edge_cost in node.children
        )
    else:  # AND node
        # Sum of all children + edge cost
        return sum(
            (
                sum(cost_table[c.name] for c in child) + edge_cost
                if isinstance(child, list)
                else cost_table[child.name] + edge_cost
            )
            for child, edge_cost in node.children
        )


def ao_star(node, cost_table=None, solved=None):
    
    if cost_table is None:
        cost_table = {}
    if solved is None:
        solved = {}

    # If already solved
    if node.name in solved:
        return cost_table[node.name]

    # Base case: leaf node
    if not node.children:
        cost_table[node.name] = node.h
        solved[node.name] = True
        return node.h

    # Recursively solve subproblems
    for child, _ in node.children:
        if isinstance(child, list):  # AND group
            for c in child:
                ao_star(c, cost_table, solved)
        else:
            ao_star(child, cost_table, solved)

    # Compute cost
    cost_table[node.name] = compute_cost(node, cost_table)

    # Check if all children are solved
    all_solved = True
    for child, _ in node.children:
        if isinstance(child, list):
            if not all(solved.get(c.name, False) for c in child):
                all_solved = False
        else:
            if not solved.get(child.name, False):
                all_solved = False

    if all_solved:
        solved[node.name] = True

    return cost_table[node.name]


# ---------------- USER INPUT -----------------
nodes = {}
n = int(input("Enter number of nodes: "))

# Create nodes
for _ in range(n):
    name = input("Enter node name: ").strip()
    node_type = input("Enter type (OR/AND): ").upper()
    heuristic = int(input(f"Enter heuristic value for {name}: "))
    nodes[name] = Node(name, node_type, heuristic)

# Add edges
e = int(input("Enter number of edges: "))
for _ in range(e):
    line = input("Enter edge (parent children cost): ")
    # Example: A B 1   or   A (C,D) 2
    parts = line.split()
    u, v, c = parts[0], parts[1], int(parts[2])

    if v.startswith("(") and v.endswith(")"):
        children_names = v.strip("()").split(",")
        children = [nodes[name.strip()] for name in children_names]
        nodes[u].add_child(children, c)  # AND-group
    else:
        nodes[u].add_child(nodes[v], c)  # single child

# Root node
root_name = input("Enter root node: ").strip()
root = nodes[root_name]

# Run AO*
final_cost = ao_star(root)
print("\nOptimal solution cost from root:", final_cost)


"""