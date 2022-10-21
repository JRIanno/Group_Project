from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users


class Carmeets:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.location = data['location']
        self.date_time = data['date_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']


    @classmethod
    def create_meet(cls, data):
        query = 'INSERT INTO carmeets (name, type, location, date_time, creator_id) VALUES (%(name)s, %(type)s, %(location)s, %(date_time)s, %(creator_id)s);'
        print("Running Query: 'INSERT INTO carmeets (name, type, location, date_time, creator_id) VALUES (%(name)s, %(type)s, %(location)s, %(date_time)s, %(creator_id)s);'")
        return connectToMySQL('meets').query_db(query, data)

    @classmethod
    def follow(cls, data):
        query = 'INSERT INTO following (follow_id, meet_id) VALUES (%(follow_id)s, %(meet_id)s);'
        return connectToMySQL('meets').query_db(query, data)

    @classmethod
    def get_club_id(cls):
        query = 'SELECT * FROM carmeets JOIN users ON users.id = carmeets.creator_id;'
        meet_data = connectToMySQL('meets').query_db(query)

        carmeets = []
        for meet in meet_data:
            cm = cls(meet)
            cm.users = users.Users(
                {
                    'id': meet['creator_id'],
                    'first_name': meet['first_name'],
                    'last_name': meet['last_name'],
                    'email': meet['email'],
                    'password': meet['password'],
                    'created_at': meet['users.created_at'],
                    'updated_at': meet['users.updated_at'],
                }
            )
            carmeets.append(cm)

        return carmeets

    @classmethod
    def first_left_join(cls, data):
        query = 'SELECT * FROM carmeets LEFT JOIN following ON meet_id = carmeets.id LEFT JOIN users ON following.follow_id = users.id WHERE carmeets.creator_id = %(id)s;'
        results = connectToMySQL('meets').query_db(query, data)

        carmeets = []
        for meet in results:
            cm = cls(meet)
            cm.users = users.Users(
                {
                    'id': meet['creator_id'],
                    'first_name': meet['first_name'],
                    'last_name': meet['last_name'],
                    'email': meet['email'],
                    'password': meet['password'],
                    'created_at': meet['users.created_at'],
                    'updated_at': meet['users.updated_at'],
                }
            )
            carmeets.append(cm)

        return carmeets

    @classmethod
    def meet_up(cls,carmeets_id):
        data = {'id': carmeets_id}
        query = 'SELECT * FROM carmeets LEFT JOIN following ON meet_id = carmeets.id LEFT JOIN users ON following.follow_id = users.id WHERE carmeets.id = %(id)s;'
        result = connectToMySQL('meets').query_db(query, data)

        result = result[0]
        meet = cls(result)
        meet.users = users.Users(
            {
                'id': result['creator_id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at'],
            }
        )
        return meet

    @classmethod
    def get_all_clubs(cls, data):
        query = 'SELECT * FROM carmeets LEFT JOIN following ON meet_id = carmeets.id LEFT JOIN users ON following.follow_id = users.id WHERE carmeets.id =;'
        results = connectToMySQL('meets').query_db(query, data)

        carmeets = []
        for meet in results:
            cm = cls(meet)
            cm.users = users.Users(
                {
                    'id': meet['creator_id'],
                    'first_name': meet['first_name'],
                    'last_name': meet['last_name'],
                    'email': meet['email'],
                    'password': meet['password'],
                    'created_at': meet['users.created_at'],
                    'updated_at': meet['users.updated_at'],
                }
            )
            carmeets.append(cm)

        return carmeets

    @classmethod
    def update(cls, data):
        query = 'UPDATE carmeets SET name = %(name)s, type = %(type)s, location = %(location)s, date_time = %(date_time)s WHERE carmeets.id = %(id)s;'
        result = connectToMySQL('meets').query_db(query, data)

        return result

    @classmethod
    def delete(cls, carmeets_id):
        data = {'id': carmeets_id}
        query = 'DELETE FROM carmeets WHERE id = %(id)s;'
        connectToMySQL('meets').query_db(query, data)
        return carmeets_id