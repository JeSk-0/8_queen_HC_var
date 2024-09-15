import random


def setChessBoard():
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


def printBoard(state):
    size = len(state)
    for row in range(size):
        print(" ".join("Q" if state[row] == col else "-" for col in range(size)))


def run_simulations(num_simulations):
    """Run multiple simulations and return the best results."""
    successes = 0
    steps_successful = []
    steps_stuck = []
    best_solution = None
    best_attacking_pairs = 0
    best_steps = float('inf')
    
    for i in range(num_simulations):
        state = setChessBoard()
        final_state, final_attacking_pairs, steps = hill_climbing(state)
        
        if final_attacking_pairs == 0:
            successes += 1
            steps_successful.append(steps)
        else:
            steps_stuck.append(steps)
        
        # Track the best solution found
        if (final_attacking_pairs < best_attacking_pairs or
            (final_attacking_pairs == best_attacking_pairs and steps < best_steps)):
            best_solution = final_state
            best_attacking_pairs = final_attacking_pairs
            best_steps = steps
    
    success_probability = successes / num_simulations
    avg_steps_success = sum(steps_successful) / successes if successes > 0 else 0
    avg_steps_stuck = sum(steps_stuck) / (num_simulations - successes) if (num_simulations - successes) > 0 else 0
    
    return (success_probability, avg_steps_success, avg_steps_stuck, 
            best_solution, best_attacking_pairs, best_steps)



# Parameters
num_simulations = 1000
best_results = None
best_probability = 0

# Run simulations
print("Running first choice hill-climbing simulations...")
results = run_simulations(num_simulations)

# Check if the current results have a better probability
if results[0] > best_probability:
    best_probability = results[0]
    best_results = results

# Print the best results
if best_results:
    print("\nBest Results Found:")
    print(f"Success Probability: {best_results[0] * 100:.2f}%")
    print(f"Average Steps when Successful: {best_results[1]}")
    print(f"Average Steps when Stuck: {best_results[2]}")
    print("\nBest Solution Found:")
    printBoard(best_results[3])
    print(f"Attacking Pairs: {best_results[4]}")
    print(f"Steps to Find Solution: {best_results[5]}")



