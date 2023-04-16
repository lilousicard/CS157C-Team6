import models
from models import graph, matcher, rel_matcher, Node, Relationship


class Restaurants:

    def __init__(self):
        pass

    @staticmethod
    def get_all():
        rests = matcher.match("Restaurant")
        return list(rests)