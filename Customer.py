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
        owner = params.get("restaurant_owner")
        image_path = params.get("image_path")
        # encrypt pass later with bcrypt
        if not self.find():
            if not owner:
                cust = Node("Customer", email=self.email,
                            name=name, password=password, gender=gender,
                            age=age, image_path=image_path)
                graph.create(cust)
                return True
            else:
                owner = Node("Owner", email=self.email, name=name,
                             password=password, gender=gender, age=age, image_path=image_path)
                graph.create(owner)
                return True
        else:
            return False

    def add_friend(self, friend_email):
        cur_user = self.find()
        # search for the user that has been sent a friend request
        friend_node = matcher.match("Customer", email=friend_email).first()
        # create connection of friend_node was found(Should be no error)
        if friend_node:
            graph.create(Relationship(cur_user, "FRIENDS", friend_node))
        else:
            print(f"User {friend_email} doesn't exist")

    def get_friends(self):
        cust = self.find()
        friends = rel_matcher.match((cust, None), "FRIENDS")
        return [r.end_node for r in friends]

    def is_friends(self, other_email):
        cur_user = self.find()
        other_user = models.get_customer(other_email)
        return rel_matcher.match(nodes=[cur_user, other_user],
                                 r_type="FRIENDS")





