from copy import deepcopy

# ---------------------------------------------
# Helper functions for 8-puzzle representation
# ---------------------------------------------

# Goal state
GOAL_STATE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]   # 0 represents the blank tile
]


def is_goal(state):
    """Check if the current state is the goal."""
    return state == GOAL_STATE


def find_blank(state):
    """Find (row, col) position of the blank (0)."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def successors(state):
    """Generate all possible moves (neighbors) by sliding one tile."""
    r, c = find_blank(state)
    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = deepcopy(state)
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            neighbors.append(new_state)
    return neighbors


# ---------------------------------------------
# IDDFS Algorithm (with iteration display)
# ---------------------------------------------

def iddfs(root, is_goal, successors, max_depth=20):
    """
    Iterative Deepening Depth-First Search (IDDFS)
    """
    for limit in range(max_depth + 1):
        print(f"\n=== Iteration (Depth Limit = {limit}) ===")
        visited = set()
        result = dls(root, limit, visited, is_goal, successors, depth=0)
        if result not in ("cutoff", "failure", None):
            print(f"\n✅ Goal found at depth {limit}")
            return result, limit
    print("\n❌ Goal not found within depth limit.")
    return None, None


def dls(node, limit, visited, is_goal, successors, depth):
    """Depth-Limited Search (recursive) with printing."""
    print(f"Exploring node at depth {depth}: {node}")

    if is_goal(node):
        print("🎯 Goal reached!")
        return node
    if limit == 0:
        return "cutoff"

    visited.add(tuple(map(tuple, node)))
    cutoff_occurred = False

    for neighbor in successors(node):
        key = tuple(map(tuple, neighbor))
        if key in visited:
            continue
        result = dls(neighbor, limit - 1, visited, is_goal, successors, depth + 1)
        if result == "cutoff":
            cutoff_occurred = True
        elif result != "failure" and result is not None:
            return result

    visited.remove(tuple(map(tuple, node)))

    if cutoff_occurred:
        return "cutoff"
    else:
        return "failure"


# ---------------------------------------------
# Example Test Run
# ---------------------------------------------

if __name__ == "__main__":
    # Example initial state (solvable)
    initial_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

    print("Initial State:")
    for row in initial_state:
        print(row)

    result, depth = iddfs(initial_state, is_goal, successors, max_depth=10)

    if result is not None:
        print("\nFinal Goal State:")
        for row in result:
            print(row)
