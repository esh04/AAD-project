from random import randrange, seed
from datetime import datetime
seed(datetime.now())

def rand_num():
    return randrange(1,10)

def guess_socks(correct, guess, wrong_answers):
    while wrong_answers < 4:
        if guess == correct:
            print("That's right! It's", correct)
            break
        else:
            print("That's wrong!")
            if guess>correct:
                print("Too High!")
            elif guess<correct:
                print("Too low!")
            wrong_answers += 1
    else:
        print("It's" , correct)

    return wrong_answers

