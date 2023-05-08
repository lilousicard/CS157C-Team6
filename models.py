from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os

url = os.environ.get("neo4j+s://ea1daa0c.databases.neo4j.io",
                     "bolt://localhost:7687")

graph = Graph("neo4j+s://3f3038da.databases.neo4j.io",
              auth=("neo4j", "NW4jLYvV9n2m47clB6ht7GUMGBKKyhrC5wivIC8nFBo"))

# graph = Graph("neo4j+s://ea1daa0c.databases.neo4j.io",
#               auth=("neo4j", "4CZLYw1ngU7jYPn_LTZi0lUTa7jJoerx2bSb3q8M6lo"))


matcher = NodeMatcher(graph)
rel_matcher = RelationshipMatcher(graph)


def search_node(node, search_term, exclude_term):
    target_node = node.capitalize()
    # search for nodes that have attributes that match the search term,
    # but exclude password, email, and image path
    results = matcher.match(target_node).where(
        f"any(attr in keys(_) where attr <> 'password' and attr <> 'email' "
        f"and attr <> 'image_path' and _["f"attr]  =~ '("f"?i)."
        f"*{search_term}.*')"
    )

    # if searching for users, exclude the currently logged-in user
    if target_node == "Customer" and exclude_term is not None:
        results = results.where(f"_.email <> '{exclude_term}'")

    return [dict(node) for node in results]


def get_customer(email):
    return matcher.match("Customer", email=email).first()


def get_rest_in_city(restaurants, city):
    # Returns the city that the restaurant is Located in
    # get the city node
    city_node = matcher.match("City", name=city).first()

    # get all restaurants and see which ones are located in <city>
    city_rest = [r for r in restaurants if
                 rel_matcher.match(nodes=(r, city_node), r_type="Location")]

    return city_rest


def get_cust_city(customer):
    # returns the city that the customer Reside in
    cust_node = matcher.match("Customer", email=customer).first()
    city_rel = rel_matcher.match(nodes=(cust_node,), r_type="Reside").first()
    return city_rel.end_node.get("name")


def get_restaurant(name):
    return matcher.match("Restaurant", name=name).first()


def get_rest_city(rest_node):
    return rel_matcher.match(nodes=(rest_node,), r_type="Located").first(). \
        end_node.get("name")

