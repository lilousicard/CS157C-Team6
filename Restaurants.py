import models
from models import graph, matcher, rel_matcher, Node, Relationship


class Restaurants:

    def __init__(self, name):
        self.name = name


    @staticmethod
    def get_all():
        rests = matcher.match("Restaurant")
        return list(rests)

    def store_rating(self, rating, review, user_email):
        #create node rating
        rating = Node("Rating", Comment = review, score = rating)
        graph.create(rating)
        #restaurant link ?
        restau_node = models.get_restaurant(self.name)
        # restau_node should be present
        graph.create(Relationship(restau_node, "REVIEW", rating))
        #customer link?
        cust = models.get_customer(user_email)
        graph.create(Relationship(cust, "MADE", rating))

    def create_like(self, r_name, user_email):
        restau_node = models.get_restaurant(self.name)
        cust = models.get_customer(user_email)
        graph.create(Relationship(cust, "LIKES", restau_node))

    def delete_like(self, r_name, user_email):
        query = '''
               MATCH (a:Customer{email: '%s'})-[r:LIKES]->(b:Restaurant {name: '%s'}) 
               DELETE r
               ''' % (user_email, r_name)
        list = graph.run(query)
        print(list)
