# ceng495hw1
Name: Mustafa İlbey Deniz
Student ID: 2448314

an e-commerce website deployed with Render and MongoDB Atlas

to build:
```
pip3 install -r requirements.txt
cd cowShop
yarn run build
python3 run.py
```

# What did I do?
I used Vue(Vuetify) and Flask. Flask is extremly easy to learn and pymongo is also useful for mongoDB connection.
All of the backend requests have been done over socketIO. 

I implemented login and signup pages which are accessible from them human icon on the right corner.
For authentication, I used JWT and stored it in localStorage (which is not the safest one, however it is useful)


On signup page, user can choose between 2 account types: Admin and Regular. Regular users does not have access to 
'/admin' route(which can be seen as a wrench icon on top right after logging in), therefore it can't add/remove items/users.

I left the the user type choice available for the sake of testing easier.

All users can add review/rating, and update them.

User statistics can be viewed in human icon that is used for logging in before.

Products does not have static fields in the database. Different type of items have uncommon fields.

User can view the products, however he/she needs to be logged in for that, otherwise an alert will be shown up.

Product/User deletion will update other tables accordingly.


# An example admin account:
username: newadmin
password: 1