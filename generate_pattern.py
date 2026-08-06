import itertools

LENGTH = 4

def generate_relative_permutations(length):
    # Generate all possible permutations with replacement
    all_combos = itertools.product(range(1, length + 1), repeat=length)
    
    valid_permutations = []
    
    for combo in all_combos:
        # Rule 1: The lowest number must be 1 (eliminates relative duplicates > 1)
        if min(combo) != 1:
            continue
            
        # Rule 2: Eliminate permutations where all positions are the same
        if len(set(combo)) == 1:
            continue
            
        # Format as a string with dashes
        valid_permutations.append("-".join(map(str, combo)))
        
    return valid_permutations

if __name__ == "__main__":
    for r in generate_relative_permutations(LENGTH):
        print(r)
