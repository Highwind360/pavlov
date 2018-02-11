# TODO: add the root as a variable
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

DATABASE_URL = "sqlite:///%s/pavlov.db" % ROOT

COOKIE_COST = 20
