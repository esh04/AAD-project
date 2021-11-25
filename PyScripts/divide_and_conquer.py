from random import randrange, seed
from datetime import datetime
seed(datetime.now())
import math

def rand_num(i,j):
    return randrange(i,j)

def guess_socks(correct, guess, wrong_answers, max):
    if wrong_answers < max:
        if guess == correct:
            return "You are correct! It was sock number {}".format(correct), wrong_answers
        else:
            wrong_answers += 1
            if wrong_answers == max:
                return  "Game over. The smelly sock was sock {}. Press Restart to play again".format(correct), wrong_answers

            if guess>correct:
                return "Your guess was too high. You have {} more tries".format(math.ceil(max) - wrong_answers), wrong_answers 
            elif guess<correct:
                return "Your guess was too low. You have {} more tries".format(math.ceil(max)- wrong_answers), wrong_answers 

