from collections import deque

def missionaries_cannibals_solver(total_m, total_c, capacity=2):
    MOVES = [(m, c) for m in range(capacity + 1)
                     for c in range(capacity + 1)
                     if 1 <= m + c <= capacity]

    def is_valid(ML, CL):
        MR, CR = total_m - ML, total_c - CL
        # missionaries and cannibals within bounds
        if not (0 <= ML <= total_m and 0 <= CL <= total_c):
            return False
        # left bank safety
        if ML > 0 and CL > ML:
            return False
        # right bank safety
        if MR > 0 and CR > MR:
            return False
        return True

    def next_states(state):
        ML, CL, boat = state
        for m, c in MOVES:
            if boat == 'L':   # boat goes left -> right
                nML, nCL = ML - m, CL - c
                nboat = 'R'
            else:             # boat goes right -> left
                nML, nCL = ML + m, CL + c
                nboat = 'L'
            if nML >= 0 and nCL >= 0 and is_valid(nML, nCL):
                yield (nML, nCL, nboat), (m, c)

    def bfs():
        start = (total_m, total_c, 'L')
        goal = (0, 0, 'R')
        q = deque([start])
        parent = {start: None}
        move_taken = {start: None}
        while q:
            s = q.popleft()
            if s == goal:
                path, moves = [], []
                cur = s
                while cur is not None:
                    path.append(cur)
                    moves.append(move_taken[cur])
                    cur = parent[cur]
                return path[::-1], moves[::-1]
            for ns, mv in next_states(s):
                if ns not in parent:
                    parent[ns] = s
                    move_taken[ns] = mv
                    q.append(ns)
        return None, None

    return bfs()


# Example: solve for 3 missionaries, 3 cannibals
path, moves = missionaries_cannibals_solver(3, 3, capacity=2)

print("\n=== Missionaries and Cannibals (Generalized) ===")
if path:
    for i in range(1, len(path)):
        prev_state = path[i-1]
        next_state = path[i]
        m, c = moves[i]
        print(f"Step {i}: {prev_state} -> {next_state}, boat carries {m} M, {c} C")
else:
    print("No solution found.")
