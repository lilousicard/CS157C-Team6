# CS157C-Team6

## **Team Members**

1. Jesse Dong
2. Samyak Jagdish Kumbhalwar
3. Lilou Sicard-Noel

## **NoSql Database**

Neo4j (https://neo4j.com/)

<img width="871" alt="Screenshot 2023-05-11 at 12 41 44 PM" src="https://github.com/lilousicard/CS157C-Team6/assets/11585585/405fa9c0-2f9a-49a4-bf6c-fbf5ed239e5b">
 
Node Type

Customer
- Age: Int
- Email: String
- Gender: String
- Name: String
- Password: String

Owner
- Age: Int
- Email: String
- Gender: String
- Name: String
- Password: String

Restaurant
- Name: String
- Type: String

City
- Name: String
- State: String
- Country: String

Rating
- Comment: String
- Score: Int (out of 5)

Relationship

Customer -> Made -> Rating

Restaurant -> Review -> Rating

Customer -> Friends -> Customer (Try to avoid duplicate)

Restaurant -> Location -> City

Owner -> Owns -> Restaurant

Customer -> Likes -> Restaurant



