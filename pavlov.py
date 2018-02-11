"""
pavlov.py
highwind

A tool for counting how many push-ups you've done, and determining the reward.
"""

from numpy import cos, pi
from itertools import count

from .settings import COOKIE_COST
from .database import Session, Exercise, ExerciseSet


def ceil(n):
    return (n // 1) + 1

def input_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("That's not a number.")
    return 0

def score_by_ratio(goal, done):
    """Calculates a score based on a ratio of goal to accomplishment

    Params:
        goal - the number you aimed to do
        done - the number you did
    
    Returns: a float between 0-2, granting you a score"""
    return 1 - cos((pi/2)*(done/goal))

# TODO: just return the points unspent
def calculate_user_score(sess):
    """Given a user, what points have they scored total?"""
    points = 0
    for ex in sess.query(Exercise).all():
        # TODO: just consider the reps from today
        total_ex_reps = sum(map(lambda x: x.reps, ex.exercise_sets))
        if total_ex_reps > 2 * ex.goal:
            print("Warning: You met over twice your goal for '%s'.\nThis " + \
                  "means your goal is too low. Your score has been penalized for it.")
        rep_score = score_by_ratio(ex.goal, total_ex_reps)
        points += int(ceil(ex.value * rep_score))
    return points

def exercise_menu(sess):
    """Displays the exercises available and adds reps to one of the user's choice."""
    choices = {}
    exercises = sess.query(Exercise).order_by(Exercise.name).all()
    back = len(exercises) + 1

    # Display the exercise menu prompt
    print("Which exercise did you do?")
    for i, e in zip(count(1), exercises):
        print("%i. %s" % (i, e.name))
        choices[i] = e
    print("%i. Go back" % back)

    # Have the user select an option
    choice = input_int("\nYour choice => ")
    while choice not in range(1, len(exercises)+1):
        if choice == back:
            return
        choice = input_int("Sorry. Try again => ")

    exercise = choices[choice]
    reps = input_int("How many %s did you do? " % exercise.name)
    ex_set = ExerciseSet(reps=reps, exercise=exercise)
    sess.add(ex_set)
    sess.commit()

def main():
    # TODO: make the exercise menu a submenu
    #       dynamically created from config
    # TODO: add more rewards than cookies
    # TODO: disallow cookie debt
    # TODO: allow points to expire
    print("Welcome to the incentivizer.")

    c_score = 0
    session = Session()
    try:
        while True:
            choice = input_int("What would you like to do?\n" + \
                  "1. Report an exercise\n" + \
                  ("2. Spend Points on cookies (%i points each)\n" % COOKIE_COST) + \
                  "3. Show balance\n" + \
                  "4. Quit\n\nYour choice => ")

            # TODO: allow user to add exercises
            if choice == 1:
                exercise_menu(session)
            elif choice == 2:
                # TODO: allow user to choose/add rewards
                c_score = input_int("How many cookies have you eaten? ") * COOKIE_COST
                print()
            elif choice == 3:
                score = calculate_user_score(session)
                print("You've earned %i and spent %i of it on cookies." %
                    (score, c_score), end=" ")
                print("You have %i remaining.\n" % (score - c_score))
            elif choice == 4:
                print("Goodbye!")
                return
            else:
                print("Sorry. I couldn't understand your input.")
    except KeyboardInterrupt:
        pass
    print("Goodbye!")
    session.close()
