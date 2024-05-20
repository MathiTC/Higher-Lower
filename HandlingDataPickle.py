import pickle


def data_store_pickle(filename, data):
    # Open the file in write mode (overwriting any existing content)
    with open(f'{filename}.pk', "wb") as dbfile:
        # Write the data to the file
        pickle.dump(data, dbfile)
        dbfile.close()


def data_load_pickle(filename):
    try:
        dbfile = open(f'{filename}.pk', "rb")
        loaded_data = pickle.load(dbfile)
        dbfile.close()
        return loaded_data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except pickle.UnpicklingError:
        print(f"Error: Failed to unpickle data from file '{filename}'.")
        return None
