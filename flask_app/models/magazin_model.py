from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.controllers.user import User


class Magazin:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.name=data['name']
        self.description=data['description']
        self.user_id=data['user_id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod 
    def get_magazines(cls):
        query = "select*from magazines join users on users.id=user_id"
        users_paints = connectToMySQL("magazin_db").query_db(query)
        orders = []
        for users in users_paints:
            data={
                'id':users['users.id'],
                'first_name':users['first_name'],
                'last_name':users['last_name'],
                'email':users['email'],
                'password':users['password'],
                'created_at':users['users.created_at'],
                'updated_at':users['users.updated_at']
            }
            user=User(data)
            user.magazine=Magazin(users)
            orders.append(user)
        return orders


    @classmethod
    def get_details(cls, data):
        query = "select*from  magazines join users on users.id=user_id where magazines.id=%(id)s"
        user_order = connectToMySQL("magazin_db").query_db(query, data)
    
        for users in user_order:
            data = {
                'id': users['users.id'],
                'first_name': users['first_name'],
                'last_name': users['last_name'],
                'email': users['email'],
                'password': users['password'],
                'created_at': users['users.created_at'],
                'updated_at': users['users.updated_at']
            }
            user = User(data)
            user.magazine = Magazin(users)

        return user

    @classmethod
    def insert(cls, data):
        query = "insert into magazines(name,description,user_id) value(%(name)s, %(description)s,%(user_id)s)"
        return connectToMySQL("magazin_db").query_db(query, data)
 
    @classmethod
    def user_magazine(cls,data):
        query="select*from magazines where user_id=%(id)s"
        results=connectToMySQL("magazin_db").query_db(query, data)
        order=[]
        for magazine in results:
            order.append(Magazin(magazine))
        return order

    @classmethod
    def delete(cls, data):
        query = "delete from magazines where magazines.id=%(id)s"
        return connectToMySQL("magazin_db").query_db(query, data)
   
    @staticmethod
    def magazine_checker(form):
        valid = True

        if len(form['name']) < 2:
            flash("first name must have at least 2 character")
            valid = False
        if len(form['description']) < 10:
            flash("description must have at least 10 character")
            valid = False
        return valid