"""
pavlov.py
highwind

A tool for counting how many push-ups you've done, and determining the reward.
"""

from numpy import cos, pi

from .settings import COOKIE_COST, EXERCISES


def ceil(n):
    return (n // 1) + 1

def score_repcount(goal, done):
    """Calculates your exercise score based on reps.

    Params:
        goal - the number of reps you aimed to do
        done - the reps you did
    
    Returns: a float between 0-2, granting you a score"""
    if done > 2 * goal:
        raise ValueError("Your goals are too low.")

    return 1 - cos((pi/2)*(done/goal))

def calculate_exercise_score(exercise):
    """Given an exercise, how well did the user score on that exercise?."""
    reps = int(input("How many %s did you do? " % exercise["name"]))
    return int(ceil(exercise["value"] * score_repcount(exercise["goal"], reps)))

def main():
    # TODO: make the exercise menu a submenu
    #       dynamically created from config
    # TODO: save the state of things
    # TODO: add more rewards than cookies
    # TODO: allow user to add exercises/other incentives
    # TODO: allow user to add rewards
    print("Welcome to the incentivizer.")

    score = {}
    c_score = 0
    running = True
    try:
        while running:
            choice = input("What would you like to do?\n" + \
                  "1. Report an exercise\n" + \
                  ("2. Spend Points on cookies (%i points each)\n" % COOKIE_COST) + \
                  "3. Quit\nYour choice => ")

            if int(choice) == 1:
                score["Push-Up"] = calculate_exercise_score(EXERCISES["Push-Up"])
            elif int(choice) == 2:
                c_score = int(input("How many cookies have you eaten? ")) * COOKIE_COST
            elif int(choice) == 3:
                running = False
            else:
                print("Sorry. I couldn't understand your input.")

            total_score = sum(score.values())
            print("You've earned %i and spent %i of it on cookies." %
                (total_score, c_score), end=" ")
            print("You have %i remaining." % (total_score - c_score))
    except KeyboardInterrupt:
        pass
    print("Goodbye!")
