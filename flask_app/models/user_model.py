from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def insert_user(cls,data):
        exist=User.check_account(data)
        if exist!= False:
            query = "INSERT INTO users (first_name , last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
            return connectToMySQL("magazin_db").query_db(query,data)
        else:
            return exist 


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("magazin_db").query_db(query,data)

        if len(user_db) < 1:
            return False
        
        return User(user_db[0])

    @classmethod
    def update(cls,data):
        query='UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s where users.id=%(id)s' 
        return connectToMySQL("magazin_db").query_db(query, data)
        

    @staticmethod
    def form_checker(form):
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        valid=True
         
        if len( form['first_name'])<2:
            flash("first name must have at least 2 character")
            valid = False
        if len( form['last_name'])<2:
            flash("last name must have at least 2 character")
            valid = False                  
        if not email_reg.match(form["email"]):
            flash("Invalid Email")
            valid = False
        if len( form['password'])<8:
            flash("passeword must have at least 8 character")
            valid = False
        if not form['password'] == form['confirm_password']:
            flash("passwords don't match")
            valid = False  
        return valid

    @staticmethod
    def update_checker(form):
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        valid = True

        if len(form['first_name']) < 2:
            flash("first name must have at least 2 character")
            valid = False
        if len(form['last_name']) < 2:
            flash("last name must have at least 2 character")
            valid = False
        if not email_reg.match(form["email"]):
            flash("Invalid Email")
            valid = False
        return valid

    @staticmethod
    def check_account(data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("magazin_db").query_db(query, data)

        if len(user_db)>0:
            return False
  
        return True


    