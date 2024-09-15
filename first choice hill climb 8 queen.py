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


def random_neighbor(state):
        """
        Generate a random neighbor by moving a queen in a random column to a random row.
        """
        new_queens = list(state)
        col = random.randint(0, 100000)%8  # Randomly choose a column
        row = random.randint(0, 100000)%8  # Randomly choose a new row for the queen
        new_queens[col] = row
        return new_queens

def printBoard(state):
    size = len(state)
    for row in range(size):
        print(" ".join("Q" if state[row] == col else "-" for col in range(size)))

def first_choice_hill_climbing(state,max_steps=1000):
    # Start with a random board
    steps=0
    neighbor=[]
    current_h=calculate_attacking_pairs(state)
    while steps < max_steps:
        steps += 1
        current_h = calculate_attacking_pairs(state)

        if current_h == 0:
            return state,current_h,steps

        # Get a random neighbor
        neighbor=random_neighbor(state)
        neighbor_h = calculate_attacking_pairs(neighbor)

        # If the neighbor has fewer conflicts, move to the neighbor
        if neighbor_h < current_h:
            state = neighbor
            current_h=neighbor_h

    return state,current_h,steps



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
        final_state, final_attacking_pairs, steps = first_choice_hill_climbing(state)
        
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


