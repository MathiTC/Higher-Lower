import math

# Funktion der beregner værdien efter et brugerinput
def calculate (rating_1, rating_2):
    def calculate_elo(rating_winner, rating_loser, K=32, result=1):
        expectation_winner = 1 / (1 + math.pow(10, (rating_loser - rating_winner) / 400))
        expectation_loser = 1 / (1 + math.pow(10, (rating_winner - rating_loser) / 400))

        new_rating_winner = rating_winner + K * (result - expectation_winner)
        new_rating_loser = rating_loser + K * ((1 - result) - expectation_loser)

        return {'winner': new_rating_winner, 'loser': new_rating_loser}