"""
Music Snippet Generator

This script generates musical note snippets based on predefined scale interval 
patterns (e.g., "1-2-3"). It maps these numerical patterns to actual pitches 
within a specified diatonic range (from START_NOTE to END_NOTE) using LilyPond 
notation. The script calculates the relative offsets for each pattern, generates 
the sequential snippets, and saves the final output as a JSON array in 'snippet.json'.
"""

import json

# --- Configuration Constants ---
DIATONIC_SCALE = [
    "c", "d", "e", "f", "g", "a", "b",
    "c'", "d'", "e'", "f'", "g'", "a'", "b'",
    "c''", "d''", "e''", "f''", "g''", "a''", "b''",
    "c'''", "d'''", "e'''", "f'''", "g'''", "a'''", "b'''"
]

START_NOTE = "c'"
END_NOTE = "g'"

# Define the patterns to generate snippets for
PATTERNS = [
    "1-1-2", "1-1-3", "1-2-1", "1-2-2", "1-2-3", "1-3-1", "1-3-2", "1-3-3", "2-1-1", "2-1-2", "2-1-3", "2-2-1", "2-3-1", "3-1-1", "3-1-2", "3-1-3", "3-2-1", "3-3-1",
]

def generate_configs_for_pattern(sequence_name: str) -> list:
    """
    Generates a list of configuration dictionaries for a single sequence pattern.
    """
    try:
        steps = [int(x) for x in sequence_name.split("-")]
    except ValueError:
        raise ValueError(f"Sequence '{sequence_name}' must be numbers separated by hyphens.")
    
    # Calculate zero-based relative offsets from the base note (1)
    offsets = [step - 1 for step in steps]
    
    if START_NOTE not in DIATONIC_SCALE or END_NOTE not in DIATONIC_SCALE:
        raise ValueError("START_NOTE or END_NOTE is outside the supported DIATONIC_SCALE list.")
        
    start_idx = DIATONIC_SCALE.index(START_NOTE)
    end_idx = DIATONIC_SCALE.index(END_NOTE)
    
    min_offset = min(offsets)
    max_offset = max(offsets)
    
    configs = []
    
    # current_base represents the index of '1' in the given sequence.
    # We shift the starting base down by min_offset to ensure the lowest 
    # note in the very first snippet exactly aligns with the start_idx.
    current_base = start_idx - min_offset
    
    # Iterate as long as the highest note in the pattern doesn't exceed the end boundary
    while current_base + max_offset <= end_idx:
        note_names = [DIATONIC_SCALE[current_base + offset] for offset in offsets]
        snippet = " ".join([f"{note}4" for note in note_names])
        
        # The note corresponding to '1' in the pattern is exactly at current_base
        note_at_1 = DIATONIC_SCALE[current_base]
        
        config = {
            "name": f"{sequence_name} {note_at_1}",
            "tempo": "120",
            "key": r"c \major",
            "snippets": [snippet]
        }
        configs.append(config)
        
        current_base += 1
        
    return configs

if __name__ == "__main__":
    all_configs = []
    
    # Process each pattern and aggregate the results
    for pattern in PATTERNS:
        try:
            pattern_configs = generate_configs_for_pattern(pattern)
            all_configs.extend(pattern_configs)
        except Exception as e:
            print(f"Error processing pattern {pattern}: {e}")
    
    # Write the aggregated configs to snippet.json
    output_filename = "snippet.json"
    try:
        with open(output_filename, "w") as outfile:
            json.dump(all_configs, outfile, indent=4)
        print(f"Successfully generated {len(all_configs)} snippets and saved to '{output_filename}'.")
    except IOError as e:
        print(f"Failed to write to file: {e}")
