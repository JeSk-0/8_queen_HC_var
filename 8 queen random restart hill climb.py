import random

def setChessBoard():
    """Generate a random 8-queens state (one queen per column)."""
    return [random.randint(1,1000000)%8 for i in range(8)]

def calculate_attacking_pairs(state):
    """Calculate the number of pairs of queens that are attacking each other."""
    attacking_pairs = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacking_pairs += 1
    return attacking_pairs

def hill_climbing(state):
    """Perform hill-climbing to minimize the number of attacking pairs."""
    current_attacking_pairs = calculate_attacking_pairs(state)
    steps = 0
    
    while True:
        steps += 1
        neighbors = []
        for col in range(8):
            for row in range(8):
                if state[col] != row:
                    new_state = list(state)
                    new_state[col] = row
                    neighbors.append((new_state, calculate_attacking_pairs(new_state)))
        
        # Sort neighbors based on number of attacking pairs (ascending order)
        neighbors.sort(key=lambda x: x[1])
        
        # Find the best neighbor (with the fewest attacking pairs)
        best_neighbor, best_attacking_pairs = neighbors[0]
        
        # Check if we can make an improvement
        if best_attacking_pairs < current_attacking_pairs:
            state = best_neighbor
            current_attacking_pairs = best_attacking_pairs
        else:
            # No improvement, return current state
            return state, current_attacking_pairs, steps

def random_restart_hill_climbing(max_restarts=100):
    """Random restart hill climbing to minimize attacking pairs in the 8-queens problem."""
    best_state = None
    fewest_attacking_pairs = float('inf')
    total_steps = 0

    for restart in range(max_restarts):
        state = setChessBoard()
        final_state, final_attacking_pairs, steps = hill_climbing(state)
        total_steps += steps
        restart+=1

        if final_attacking_pairs == 0:
            print(f"Solution found after {total_steps} steps (including restarts)and {restart} restarts!")
            return final_state, total_steps

        # Track the best solution found
        if final_attacking_pairs < fewest_attacking_pairs:
            best_state = final_state
            fewest_attacking_pairs = final_attacking_pairs

    print(f"No solution found after {max_restarts} restarts. Best solution has {fewest_attacking_pairs} attacking pairs.")
    return best_state, total_steps

def printBoard(state):
    """Display the board with queens and dots."""
    size = len(state)
    for row in range(size):
        print(" ".join("Q" if state[row] == col else "-" for col in range(size)))

# Parameters
max_restarts = 100

# Run random restart hill climbing
print("Running random restart hill-climbing algorithm...")
solution, steps = random_restart_hill_climbing(max_restarts)

# Print the best solution found
if solution:
    print("\nBest Solution Found:")
    printBoard(solution)
    print(f"Steps to Find Solution: {steps}")
else:
    print("No solution found.")
