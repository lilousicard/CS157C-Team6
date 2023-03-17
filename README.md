# CS157C-Team6

## **Team Members**

1. Jesse Dong
2. Samyak Jagdish Kumbhalwar
3. Lilou Sicard-Noel

## **NoSql Database**

Neo4j (https://neo4j.com/)
 
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
