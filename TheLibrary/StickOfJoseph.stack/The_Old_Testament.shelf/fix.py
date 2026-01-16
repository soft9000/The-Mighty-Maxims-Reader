import os
import sys

def remove_leading_underscore(filename):
    """
    Removes a leading underscore from the filename.
    """
    # Check if the filename starts with a single underscore to avoid
    # affecting double underscores (dunders) if that is a concern.
    cols = filename.split('_')
    if len(cols) > 1:
        # Create the new filename by slicing the original string
        new_filename = cols[1]
        try:
            os.rename(filename, new_filename)
            print(f"Renamed: '{filename}' -> '{new_filename}'")
        except OSError as e:
            print(f"Error renaming file '{filename}': {e}")
    else:
        print(f"No underscore found for: '{filename}'")

if __name__ == "__main__":
    import os
    for file in os.listdir():
        if file.endswith(".mmrb"):
            remove_leading_underscore(file)
            

