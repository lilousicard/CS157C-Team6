from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os

url = os.environ.get("neo4j+s://ea1daa0c.databases.neo4j.io",
                     "bolt://localhost:7687")

graph = Graph("neo4j+s://ea1daa0c.databases.neo4j.io",
              auth=("neo4j", "4CZLYw1ngU7jYPn_LTZi0lUTa7jJoerx2bSb3q8M6lo"))
matcher = NodeMatcher(graph)
rel_matcher = RelationshipMatcher(graph)


def search_node(node, search_term):
    target_node = node.capitalize()
    # search for nodes that have attributes that match the search term,
    # but exclude password and email
    # TODO: exclude logged in user as well
    results = matcher.match(target_node).where(
        f"any(attr in keys(_) where attr <> 'password' and attr <> 'email' "
        f"and _["f"attr]  =~ '("f"?i).*{search_term}.*')"
    )
    return [dict(node) for node in results]


def get_customer(email):
    return matcher.match("Customer", email=email).first()






