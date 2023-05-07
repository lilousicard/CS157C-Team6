from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os

url = os.environ.get("neo4j+s://ea1daa0c.databases.neo4j.io",
                     "bolt://localhost:7687")

graph = Graph("neo4j+s://3f3038da.databases.neo4j.io",
              auth=("neo4j", "NW4jLYvV9n2m47clB6ht7GUMGBKKyhrC5wivIC8nFBo"))

matcher = NodeMatcher(graph)
rel_matcher = RelationshipMatcher(graph)


def search_node(node, search_term, exclude_term):
    target_node = node.capitalize()
    # search for nodes that have attributes that match the search term,
    # but exclude password and email
    results = matcher.match(target_node).where(
        f"any(attr in keys(_) where attr <> 'password' and attr <> 'email' "
        f"and _["f"attr]  =~ '("f"?i).*{search_term}.*')"
    )

    # if searching for users, exclude the currently logged-in user
    if exclude_term is not None:
        results = results.where(f"_.email <> '{exclude_term}'")

    return [dict(node) for node in results]


def get_customer(email):
    return matcher.match("Customer", email=email).first()






