from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name'] #DB Columns
        self.last_name = data['last_name'] #DB Columns
        self.email = data['email'] #DB Columns
        self.password = data['password'] # DB Columns
        self.created_at = data['created_at'] #DB Columns
        self.updated_at = data['updated_at'] #DB Columns
    # Now we use class methods to query our database
    
    @classmethod
    def create(cls, data:dict): 
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);" #write the query in the workbench to test it 
        # database request
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_one_by_email(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if results:
            return cls(results[0])
        return False

    
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query) #THE RETURN IS A LIST OF DICTIONARIES
        if results: 
        # Create an empty list to append our instances of friends
            all_users = [] #becomes a list of instances
        # Iterate over the db results and create instances of users with cls. 
            for user in results: #for dictionary(user) in list of dictionaries (results line22) grab empty list (all_users line24) and append cls(user)
                all_users.append( cls(user) ) #[**Do NOT RETURN A LIST OF DICTIONARIES to HTML FOR THIS STACK -- RETURN A LIST OF INSTANCES]
            return all_users
        return False

    @classmethod
    def update_one(cls, data:dict) -> None:
        query = "UPDATE users SET first_name = %(first_name)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_one(cls, data:dict) -> None:
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validate_registration(data:dict) -> bool:
        is_valid = True

        if len(data['first_name']) < 2:
            is_valid = False
            flash("first name is required", 'err_user_first_name')

        if len(data['last_name']) < 2:
            is_valid = False
            flash("last name is required", 'err_user_last_name')

        if len(data['email']) < 2:
            is_valid = False
            flash("email is required", 'err_user_email')
        
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False

        if len(data['password']) < 8:
            is_valid = False
            flash("password is required", 'err_user_password')

        if len(data['confirm_password']) < 8:
            is_valid = False
            flash("confirm password is required", 'err_user_confirm_password')
        elif data['password'] != data['confirm_password']:
            flash("Passwords do not match", 'err_user_confirm_password')

        return is_valid

    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True

        if len(data['email']) < 2:
            is_valid = False
            flash("email is required", 'login_err_user_email')

        if len(data['password']) < 8:
            is_valid = False
            flash("password is required", 'login_err_user_password')

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'login_err_user_email')
            is_valid = False

        return is_valid