import models
from models import graph, matcher, rel_matcher, Node, Relationship


class Customer:
    def __init__(self, email):
        self.email = email

    def find(self):
        cust = matcher.match("Customer", email=self.email).first()
        return cust

    def verify_password(self, password):
        cust = self.find()
        if cust:
            return password == cust["password"]
            # return bcrypt.verify(password, cust["password"])
        else:
            return False

    def register(self, params):
        name = params.get("name")
        password = params.get("password")
        age = params.get("age")
        gender = params.get("gender")
        image_path = params.get("image_path")

        # formats the city so that the first letter of each word is capitalized
        city = params.get("city").title()

        # encrypt pass later with bcrypt
        if not self.find():
            cust = Node("Customer", email=self.email,
                        name=name, password=password, gender=gender,
                        age=age, image_path=image_path)
            graph.create(cust)
            # create city node if not exists
            city_node = matcher.match("City", name=city).first()
            if not city_node:
                new_city = Node("City", name=city)
                graph.create(new_city)
                # create Resides relationship for the new city
                graph.create(Relationship(cust, "Reside", new_city))
            else:
                graph.create(Relationship(cust, "Reside", city_node))
            return True
        else:
            return False

    def add_friend(self, friend_email):
        cur_user = self.find()
        # search for the user that has been sent a friend request
        friend_node = models.get_customer(friend_email)
        # create connection of friend_node was found(Should be no error)
        if friend_node:
            graph.create(Relationship(cur_user, "Friends", friend_node))
        else:
            print(f"User {friend_email} doesn't exist")

    def remove_friend(self, friend_email):
        cur_user = self.find()
        # search for the user that has been sent a friend request
        other_user = models.get_customer(friend_email)
        # remove connection between the two nodes
        # Don't use graph.delete, will also remove the nodes
        rel = rel_matcher.match(nodes=[cur_user, other_user],
                                r_type="Friends").first()
        graph.separate(rel)

    def get_friends(self):
        # return a list of dictionaries with each friend name and
        # image_path information
        cur_user = self.find()
        friends = rel_matcher.match((cur_user, None), "Friends")
        friend_nodes = [r.end_node for r in friends]
        friend_list = [{'name': node['name'], 'image_path': node[
            'image_path'], 'email':node['email']}
                       for node in friend_nodes]
        return friend_list

    def get_num_friends(self):
        cur_user = self.find()
        num_friends = len(graph.match((cur_user, None), "Friends"))
        return num_friends

    def is_friends(self, other_email):
        cur_user = self.find()
        other_user = models.get_customer(other_email)
        return rel_matcher.match(nodes=[cur_user, other_user],
                                 r_type="Friends")

    def get_all_liked_restaurants(self):
        cur_user = self.find()
        # a = graph.cypher.execute("MATCH (a:Person {name:'Tom Hanks})-[
        # acted:ACTED_IN]->(movies:Movie) RETURN a, acted, movies")
        liked_rest = graph.match((cur_user, None), "Likes")
        return liked_rest

    def get_review(self):
        cur_user = self.find()
        review_query = '''MATCH (c:Customer{email:'%s'} )-[:Made]->(
        r:Rating) <-[:Review]-(t:Restaurant) RETURN r.Score AS score, 
        r.Comment AS comment, t.name AS restaurant; ''' % self.email
        rating_result = graph.run(review_query).data()
        # print(rating_result)
        data = []
        for review in rating_result:
            rating_score = review["score"]
            rating_comment = review["comment"]
            restaurant_name = review["restaurant"]

            row = [rating_score, rating_comment, restaurant_name]
            data.append(row)

        return data



