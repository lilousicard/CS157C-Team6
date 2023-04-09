# CS157C-Team6

## **Team Members**

1. Jesse Dong
2. Samyak Jagdish Kumbhalwar
3. Lilou Sicard-Noel

## **NoSql Database**

Neo4j (https://neo4j.com/)

<img width="764" alt="Screenshot 2023-04-07 at 12 17 02 PM" src="https://user-images.githubusercontent.com/11585585/230664884-a2bc9c0b-74ab-4ea9-ac47-5e16281ffc3c.png">
 
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



