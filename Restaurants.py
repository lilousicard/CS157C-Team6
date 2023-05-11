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
        rating = Node("Rating", Comment = review, Score = rating)
        graph.create(rating)
        #restaurant link ?
        restau_node = models.get_restaurant(self.name)
        # restau_node should be present
        graph.create(Relationship(restau_node, "Review", rating))
        #customer link?
        cust = models.get_customer(user_email)
        graph.create(Relationship(cust, "Made", rating))

    def create_like(self, r_name, user_email):
        restau_node = models.get_restaurant(self.name)
        cust = models.get_customer(user_email)
        graph.create(Relationship(cust, "Likes", restau_node))

    def delete_like(self, r_name, user_email):
        query = '''
               MATCH (a:Customer{email: '%s'})-[r:Likes]->(b:Restaurant {name: '%s'}) 
               DELETE r
               ''' % (user_email, r_name)
        del_list = graph.run(query)
        print(del_list)

    def get_all_details(self):
        restau_details = {}
        city_query = '''
                MATCH (a:Restaurant{name: '%s'})-[r:Location]->(b:City) 
                       RETURN b.name
                       ''' % (self.name)

        rating_query = '''
                        MATCH (a:Restaurant{name: '%s'})-[r:Review]->(b:Rating) 
                               RETURN b LIMIT 5
                               ''' % (self.name)
        image_query = '''
                       MATCH (a:Restaurant{name: '%s'}) RETURN a.image_path
                       ''' % (self.name)
        image_result = graph.evaluate(image_query)
        image_result = image_result[7:]
        restau_details['name'] = self.name
        restau_details['image_path'] = image_result
        
        restau_details['city'] = graph.evaluate(city_query)
        rating = graph.run(rating_query).data()
        total_rating = 0
        avg_rating = 0
        reviews = []
        for each in rating:
            total_rating += int(each['b']['Score'] or 0)
            reviews.append(each['b']['Comment'])

        if len(rating) != 0:
            avg_rating = round(total_rating/len(rating), 1)
        restau_details['rating'] = avg_rating
        restau_details['reviews'] = reviews
        return restau_details

    def get_rests_friends_like(self, user_email):
        restau_details = []

        query = '''
                MATCH (a:Customer{email: '%s'})-[:Friends]->(b:Customer)-[r:Likes]->(c:Restaurant)-[:Location]->(d:City)
                      RETURN c,d.name;''' % (user_email)
        rest_list = graph.run(query).data()

        for x in rest_list:
            rests = {}
            rests['name'] = x['c']['name']
            rests['image_path'] = x['c']['image_path']
            rests['city'] = x['d.name']
            restau_details.append(rests)
        return restau_details