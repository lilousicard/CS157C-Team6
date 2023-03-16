from py2neo import Graph, Node, Relationship, NodeMatcher
from passlib.hash import bcrypt
import os

url = os.environ.get('neo4j+s://41890240.databases.neo4j.io', 'http://localhost:5000')

graph = Graph('neo4j+s://ea1daa0c.databases.neo4j.io', auth=('neo4j',
                                                             'secret key'))
matcher = NodeMatcher(graph)


class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = matcher.match("User", self.username).first()
        return user

    def register(self, password):
        if not self.find():
            user = Node('User', username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False
