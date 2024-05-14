import os
import pickle


# Function to check if the RGB color already exists in the context/category file
def is_duplicate_color(context_id, rgb_color):
    if os.path.exists(f"{context_id}.pk"):
        with open(f"{context_id}.pk", "rb") as f:
            data = pickle.load(f)
            for element_id, color in data.items():
                if color == rgb_color:
                    return True
    return False


# Function to store an element ID with its RGB color in the context/category file
def store_element(context_id, rgb_color):
    if not is_duplicate_color(context_id, rgb_color):
        if os.path.exists(f"{context_id}.pk"):
            with open(f"{context_id}.pk", "rb") as f:
                data = pickle.load(f)
        else:
            data = {}
        # Find the next available element ID
        element_id = max(data.keys(), default=0) + 1
        data[element_id] = rgb_color
        with open(f"{context_id}.pk", "wb") as f:
            pickle.dump(data, f)
        print(f"Storing element with RGB code '{rgb_color}' in context '{context_id}'")
        return element_id
    else:
        print("Duplicate color found.")
        return None



