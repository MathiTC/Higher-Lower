import os
import pickle


def create_context(context_text):
    # Load or initialize the main contexts dictionary
    if os.path.exists('Contexts.pk'):
        with open('Contexts.pk', 'rb') as file:
            contexts = pickle.load(file)
    else:
        contexts = {}

    # Check if the context already exists
    for context_id, context in contexts.items():
        if context == context_text:
            print("Context already exists.")
            return context_id

    # Generate a new context ID
    context_id = len(contexts) + 1

    # Save the context in the main contexts dictionary
    contexts[context_id] = context_text

    # Save the main contexts dictionary back to file
    with open('Contexts.pk', 'wb') as file:
        pickle.dump(contexts, file)

    # Create or update the context-specific file
    context_file = f'{context_id}.pk'
    if not os.path.exists(context_file):
        with open(context_file, 'wb') as file:
            elements = {}
            pickle.dump(elements, file)

    return context_id


def get_contexts():
    try:
        with open('Contexts.pk', 'rb') as file:
            contexts_data = pickle.load(file)
            # Return a list of tuples (context_id, context_text)
            return list(contexts_data.items())
    except FileNotFoundError:
        print("Contexts file not found.")
        return []


