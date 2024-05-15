import math
import pickle


def updating_elo(id_winner, id_loser, context_id, age, gender):
    age_elos = fetch_elos(context_id, age)
    gender_elos = fetch_elos(context_id, gender)

    winner_age_rating = find_rating_by_id(id_winner, age_elos)
    print(f'Winner Age Rating{winner_age_rating}')
    winner_gender_rating = find_rating_by_id(id_winner, gender_elos)
    print(f'Winner Gender Rating{winner_gender_rating}')
    loser_age_rating = find_rating_by_id(id_loser, age_elos)
    print(f'Loser Age Rating{loser_age_rating}')
    loser_gender_rating = find_rating_by_id(id_loser, gender_elos)
    print(f'Loser Gender Rating{loser_gender_rating}')

    new_winner_age, new_loser_age = calculate_elo(winner_age_rating, loser_age_rating)
    print(f'New Winner Age{new_winner_age}')
    print(f'New Loser Age {new_loser_age}')
    new_winner_gender, new_loser_gender = calculate_elo(winner_gender_rating, loser_gender_rating)
    print(f'New Winner Gender {new_winner_gender}')
    print(f'New loser Gender {new_loser_gender}')

    new_age_data = update_values(age_elos, id_winner, id_loser, new_winner_age, new_loser_age)
    new_gender_data = update_values(gender_elos, id_winner, id_loser, new_winner_gender, new_loser_gender)

    update_elo_file(context_id, age, new_age_data)
    update_elo_file(context_id, gender, new_gender_data)


def update_values(data_list, winner_id, loser_id, winner_value, loser_value):
    updated_list = []
    winner_found = False
    loser_found = False

    for item_id, value in data_list:
        if item_id == winner_id:
            updated_list.append((item_id, winner_value))
            winner_found = True
        elif item_id == loser_id:
            updated_list.append((item_id, loser_value))
            loser_found = True
        else:
            updated_list.append((item_id, value))

    if not winner_found:
        updated_list.append((winner_id, winner_value))

    if not loser_found:
        updated_list.append((loser_id, loser_value))

    return updated_list


def fetch_elos(context_id, parameter):
    try:
        with open(f'{context_id}_{parameter}.pk', 'rb') as file:
            fetched_elos = pickle.load(file)
            if isinstance(fetched_elos, dict):
                return list(fetched_elos.items())
            elif isinstance(fetched_elos, list):
                return fetched_elos
            else:
                return []
    except FileNotFoundError:
        print("Contexts file not found.")
        return []
    except EOFError:
        print("File is empty.")
        return []


def find_rating_by_id(id_to_find, data_list):
    for item_id, value in data_list:
        if item_id == id_to_find:
            return value
    return 1200  # ID not found


# Funktion der beregner værdien efter et brugerinput
def calculate_elo(rating_winner, rating_loser, k=32, result=1):
    expectation_winner = 1 / (1 + math.pow(10, (rating_loser - rating_winner) / 400))
    expectation_loser = 1 / (1 + math.pow(10, (rating_winner - rating_loser) / 400))

    new_rating_winner = rating_winner + k * (result - expectation_winner)
    new_rating_loser = rating_loser + k * ((1 - result) - expectation_loser)

    return new_rating_winner, new_rating_loser


def update_elo_file(context_id, parameter, data):
    context_file = f'{context_id}_{parameter}.pk'
    with open(context_file, 'wb') as file:
        pickle.dump(data, file)
