# CS157C-Team6

## **Team Members**

1. Jesse Dong
2. Samyak Jagdish Kumbhalwar
3. Lilou Sicard-Noel

## **Project installation**
### Using Docker

Our project can be run using docker as we have created a docker image. To do this, please download Docker desktop and then follow the following steps. 

1. docker pull jesse24/foodcomm:latest
2. docker run -d -p port:5001 jesse24/foodcomm

Replace port with any number preferably above 10,000 to avoid conflicting ports with your system. Here is an example

docker run -d -p 15000:5001 jesse24/foodcomm

3. go to localhost:port
	
Simply open your localhost at the port you have specified earlier. So if you used the  example, go to localhost:15000

### From the Github: https://github.com/lilousicard/CS157C-Team6

If for some reason the docker image isn’t working, or you would like to run our code from the github instead, follow these instructions. Make sure you have python3 installed as well as the following python libraries: Flask, Jinja2, Py2neo, passlib. 

1. Git clone https://github.com/lilousicard/CS157C-Team6.git
2. Inside the root directly simply run: python main.py or python3 main.py depending on your python installation. 
3. Go to http://127.0.0.1:5001


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



