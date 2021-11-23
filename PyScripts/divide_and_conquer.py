from random import randrange, seed
from datetime import datetime
seed(datetime.now())
import math

def rand_num(i,j):
    return randrange(i,j)

def guess_socks(correct, guess, wrong_answers, max):
    if wrong_answers < max:
        if guess == correct:
            return "You are correct! It was {}".format(correct), wrong_answers
        else:
            if wrong_answers == max:
                return  "Game over. The correct answer was {}. Press Restart to play again".format(correct), wrong_answers

            if guess>correct:
                return "Your guess was too high. You have {} more tries".format(math.ceil(max) - wrong_answers), wrong_answers + 1
            elif guess<correct:
                return "Your guess was too low. You have {} more tries".format(math.ceil(max)), wrong_answers + 1

