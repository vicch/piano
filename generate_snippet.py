"""
Music Snippet Generator

This script generates musical note snippets from all permutations (with repetition)
of a given list of notes, for a specified length. It excludes permutations that
have 3 or more consecutive identical notes. The final output is saved as a JSON
array in 'snippet.json'.
"""

import json
from itertools import product

OUTPUT = 'snippet.json'

# --- Configuration Constants ---
# List of notes to permute (LilyPond notation)
NOTES = ["c'", "d'", "e'", "f'", "g'"]

# Length of each snippet (number of notes)
LENGTH = 4


def generate_permutation_snippets(notes: list[str], length: int) -> list:
    """
    Generates a list of configuration dictionaries for all permutations
    (with repetition) of the given notes with the specified length.
    Permutations with 3 or more consecutive identical notes are excluded.
    """
    configs = []

    # Generate all combinations with repetition (Cartesian product)
    for permutation in product(notes, repeat=length):
        # Skip permutations with 3 or more consecutive identical notes
        if any(a == b == c for a, b, c in zip(permutation, permutation[1:], permutation[2:])):
            continue

        # Create the snippet string: e.g. "c'4 d'4 e'4"
        snippet = " ".join([f"{note}4" for note in permutation])

        # Name is the note sequence joined by hyphens
        name = "-".join(permutation)

        config = {
            "name": name,
            "tempo": "120",
            "key": r"c \major",
            "snippets": [snippet]
        }
        configs.append(config)

    return configs


if __name__ == "__main__":
    all_configs = generate_permutation_snippets(NOTES, LENGTH)
    try:
        with open(OUTPUT, "w") as outfile:
            json.dump(all_configs, outfile, indent=4)
        print(f"Successfully generated {len(all_configs)} snippets and saved to '{OUTPUT}'.")
    except IOError as e:
        print(f"Failed to write to file: {e}")