import models
from models import graph, matcher, rel_matcher, Node, Relationship

class Review:
    def __init__(self, customer, restaurant, rate, comment):
        self.customer = customer
        self.restaurant = restaurant
        self.rate = rate
        self.comment = comment

    def get_all_review(self):
        review_query = "MATCH (c:Customer)-[:Made]->(r:Rating)<-[:Review]-(t:Restaurant) RETURN c.name AS customer, r.Score AS score, r.Comment AS comment, t.name AS restaurant;"
        rating_result = graph.run(review_query).data()
        print(rating_result)
        data = []
        for review in rating_result:
            customer_name = review["customer"]
            rating_score = review["score"]
            rating_comment = review["comment"]
            restaurant_name = review["restaurant"]

            row = [customer_name, rating_score, rating_comment, restaurant_name]
            data.append(row)

        return data
