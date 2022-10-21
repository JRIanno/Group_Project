from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import clubs

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = []
        self.carmeets = []
        self.cars = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL('meets').query_db(query, data)

    @classmethod
    def valid_login(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('meets').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL('meets').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all_by_id(cls, data):
        query = 'SELECT * FROM users LEFT JOIN carmeets ON users.id = carmeets.creator_id WHERE users.id = %(id)s;'
        results = connectToMySQL('meets').query_db(query, data)

        users = cls(results[0])
        for db_row in results:
            meets = {
                'id': db_row['carmeets.id'],
                'creator_id': db_row['creator_id'],
                'name': db_row['name'],
                'type': db_row['type'],
                'location': db_row['location'],
                'date_time': db_row['date_time'],
                'created_at': db_row['created_at'],
                'updated_at': db_row['updated_at'],
            }
            users.carmeets.append(clubs.Carmeets(meets))
            return users

    @classmethod
    def get_follow(cls, data):
        query = 'SELECT * FROM users LEFT JOIN following on users.id = follow_id LEFT JOIN carmeets ON meet_id = carmeets.id WHERE users.id = %(id)s;'
        results = connectToMySQL('meets').query_db(query, data)

        user = cls(results[0])
        for row in results:
            if row['carmeets.id'] == None:
                break
            data = {
                'id': row['carmeets.id'],
                'name': row['name'],
                'type': row['type'],
                'location': row['location'],
                'date_time': row['date_time'],
                'type': row['type'],
                'created_at': row['carmeets.created_at'],
                'updated_at': row['carmeets.updated_at'],
                'creator_id': row['creator_id'],
            }
            user.carmeets.append(clubs.Carmeets(data))
        return user


    @staticmethod
    def validate_user(users):
        is_valid = True
        query = 'SELECT * FROM users where email = %(email)s;'
        results = connectToMySQL('meets').query_db(query, users)
        if len(results) >= 1:
            flash('Email is already in use. try another email address')
            is_valid = False
        if len(users['first_name']) <2:
            flash('please enter your first name.')
            is_valid = False
        if len(users['last_name']) <2:
            flash('please enter your last name.')
            is_valid = False
        if not EMAIL_REGEX.match(users['email']):
            flash('Please enter your email address')
            is_valid = False
        if len(users['password']) < 8:
            flash('Password must be at least 8 characters. Try again.')
            is_valid = False
        if (users['password']) != (users['confirm_password']):
            flash('Your passwords do not match. Please try again.')
            is_valid = False
        return is_valid

    