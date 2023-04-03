from py2neo import Graph, Node, Relationship, NodeMatcher
from passlib.hash import bcrypt
import os

url = os.environ.get('neo4j+s://41890240.databases.neo4j.io', 'bolt://localhost:7687')

graph = Graph('neo4j+s://41890240.databases.neo4j.io', auth=('neo4j', 'secret key'))
matcher = NodeMatcher(graph)

class Customer:
    def __init__(self, params):
        self.username = params.get('username')
        self.password = params.get('password')
        self.age = params.get('age')
        self.gender = params.get('gender')
        self.email = params.get('email')
        self.owner = params.get('restaurant_owner')

    def find(self):
        cust = matcher.match("Customer", self.username).first()
        return cust

    def register(self):
        if not self.find():
            if self.owner == None:
                cust = Node('Customer', name=self.username, password=self.password, gender=self.gender,
                        email=self.email, age=self.age)
                graph.create(cust)
                return True
            else:
                owner = Node('Owner', name=self.username, password=self.password, gender=self.gender,
                            email=self.email, age=self.age)
                graph.create(owner)
                return True
        else:
            return False
