from py2neo import Graph, Node, Relationship, NodeMatcher
from passlib.hash import bcrypt
import os

url = os.environ.get("neo4j+s://ea1daa0c.databases.neo4j.io",
                     "bolt://localhost:7687")

graph = Graph("neo4j+s://ea1daa0c.databases.neo4j.io",
              auth=("neo4j", "4CZLYw1ngU7jYPn_LTZi0lUTa7jJoerx2bSb3q8M6lo"))
matcher = NodeMatcher(graph)


def search_node(node, search_term):
    print(f"searching {search_term} in {node}")




