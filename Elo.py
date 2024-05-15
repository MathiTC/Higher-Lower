import math


# Funktion der beregner værdien efter et brugerinput
def calculate_elo(rating_winner, rating_loser, k=32, result=1):
    expectation_winner = 1 / (1 + math.pow(10, (rating_loser - rating_winner) / 400))
    expectation_loser = 1 / (1 + math.pow(10, (rating_winner - rating_loser) / 400))

    new_rating_winner = rating_winner + k * (result - expectation_winner)
    new_rating_loser = rating_loser + k * ((1 - result) - expectation_loser)

    return {'winner': new_rating_winner, 'loser': new_rating_loser}


def update_elo_file(context_id, parameter, data):
    context_file = f'{context_id}_{parameter}.pk'
    with open(context_file, 'wb') as file:
        pickle.dump(data, file)
