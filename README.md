# CS157C-Team6

## **Team Members**

1. Jesse Dong
2. Samyak Jagdish Kumbhalwar
3. Lilou Sicard-Noel

## **NoSql Database**

Neo4j (https://neo4j.com/)

<img width="968" alt="Screenshot 2023-05-11 at 12 52 27 PM" src="https://github.com/lilousicard/CS157C-Team6/assets/11585585/c1e0814c-69ac-4779-be1a-351c227ab854">
 
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



