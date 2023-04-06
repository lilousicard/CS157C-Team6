from py2neo import Graph, Node, Relationship, NodeMatcher
from passlib.hash import bcrypt
import os

url = os.environ.get("neo4j+s://ea1daa0c.databases.neo4j.io",
                     "bolt://localhost:7687")

graph = Graph("neo4j+s://ea1daa0c.databases.neo4j.io",
              auth=("neo4j", "4CZLYw1ngU7jYPn_LTZi0lUTa7jJoerx2bSb3q8M6lo"))
matcher = NodeMatcher(graph)


class Customer:
    def __init__(self, username):
        self.username = username

    def find(self):
        cust = matcher.match("Customer", username=self.username).first()
        return cust

    def verify_password(self, password):
        cust = self.find()
        if cust:
            return password == cust["password"]
            # return bcrypt.verify(password, cust["password"])
        else:
            return False

    def register(self, params):
        password = params.get("password")
        age = params.get("age")
        gender = params.get("gender")
        email = params.get("email")
        owner = params.get("restaurant_owner")
        # encrypt pass later with bcrypt
        if not self.find():
            if not owner:
                cust = Node("Customer", username=self.username,
                            password=password, gender=gender,
                            email=email, age=age)
                graph.create(cust)
                return True
            else:
                owner = Node("Owner", name=self.username,
                             password=password, gender=gender,
                             email=email, age=age)
                graph.create(owner)
                return True
        else:
            return False

    def add_friend(self, friend):
        cur_user = self.find()
        # search for the user that has been sent a friend request
        friend_node = matcher.match("Customer", username=friend).first()
        # create connection of friend_node was found(Should be no error)
        if friend_node:
            graph.create(Relationship(cur_user, "FRIENDS", friend_node))
        else:
            print(f"User {friend} doesn't exist")
