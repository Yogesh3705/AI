import random
from copy import deepcopy

# -------------------------------
# Helper functions for 4-Queens
# -------------------------------

N = 4  # 4x4 chessboard

def evaluate(state):
    """Cost = number of attacking pairs (lower is better)."""
    attacks = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def generate_neighbors(state):
    """Generate all neighbor states by moving one queen in its column."""
    neighbors = []
    for col in range(N):
        for row in range(N):
            if state[col] != row:
                new_state = state.copy()
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors

def print_board(state):
    """Display the board configuration."""
    for r in range(N):
        line = ""
        for c in range(N):
            line += " Q " if state[c] == r else " . "
        print(line)
    print()

def random_state():
    """Generate a random state."""
    return [random.randint(0, N-1) for _ in range(N)]


# -------------------------------
# Random-Restart Hill Climbing
# -------------------------------

def hill_climbing_random_restart(max_restarts=10):
    restart = 0
    while restart < max_restarts:
        current = random_state()
        current_value = evaluate(current)
        step = 0

        print(f"\n--- Restart {restart + 1}: Initial State {current} → Cost {current_value} ---")
        print_board(current)

        while True:
            step += 1
            neighbors = generate_neighbors(current)

            if not neighbors:
                break

            # Evaluate all neighbors
            neighbor_costs = [(neighbor, evaluate(neighbor)) for neighbor in neighbors]

            print(f"\nStep {step}: Neighbors and their costs")
            for i, (neighbor, cost) in enumerate(neighbor_costs):
                print(f"Neighbor {i+1}: {neighbor} → Cost = {cost}")

            # Pick best neighbor
            best_neighbor, best_value = min(neighbor_costs, key=lambda x: x[1])

            print(f"\nBest neighbor chosen: {best_neighbor} → Cost = {best_value}")

            # Check if local optimum
            if best_value >= current_value:
                print("Reached local optimum or goal.")
                if current_value == 0:  # solution found
                    print("✅ Goal Found!")
                    print_board(current)
                    return current
                else:
                    print("Local optimum reached, restarting...\n")
                    break

            # Move to better neighbor
            current = best_neighbor
            current_value = best_value
            print("Moving to better state:")
            print_board(current)

        restart += 1

    print("❌ Goal not found after maximum restarts.")
    return None


# -------------------------------
# Example Execution
# -------------------------------

if __name__ == "__main__":
    result = hill_climbing_random_restart(max_restarts=10)
