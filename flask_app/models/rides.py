from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users

DB = 'meets'

class Cars:
    def __init__(self, data):
        self.id = data['id']
        self.make = data['make']
        self.model = data['model']
        self.car_description = data['car_description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = None

    @classmethod
    def get_all_cars(cls, data):
        query = 'SELECT * FROM cars JOIN users ON users.id = cars.user_id;'
        car_data = connectToMySQL('meets').query_db(query, data)

        cars = []
        for car in car_data:
            C = cls(car)
            C.users = users.Users(
                {
                    'id': car['user_id'],
                    'first_name': car['first_name'],
                    'last_name': car['last_name'],
                    'email': car['email'],
                    'password': car['password'],
                    'created_at': car['users.created_at'],
                    'updated_at': car['users.updated_at'],
                }
            )
            cars.append(C)

        return cars


    @classmethod
    def share_car(cls, data):
        query = 'INSERT INTO cars (user_id, make, model, car_description) VALUES (%(user_id)s, %(make)s, %(model)s, %(car_description)s);'
        return connectToMySQL('meets').query_db(query, data)

    @classmethod
    def update_car(cls, data):
        query = 'UPDATE cars SET make = %(make)s, model = %(model)s, car_description = %(car_description)s WHERE cars.id = %(id)s;'
        result = connectToMySQL('meets').query_db(query, data)

        return result


    @classmethod
    def one_car(cls, car_id):
        data = {'id': car_id}
        query = 'SELECT * FROM cars JOIN users ON users.id = cars.user_id WHERE cars.id = %(id)s;'
        result = connectToMySQL('meets').query_db(query, data)

        result = result[0]
        car = cls(result)
        car.users = users.Users(
            {
                'id': result['user_id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at'],
            }
        )
        return car

    @classmethod
    def delete_car(cls, car_id):
        data = {'id': car_id}
        query = 'DELETE FROM cars WHERE id = %(id)s;'
        connectToMySQL('meets').query_db(query, data)
        return car_id



    @staticmethod
    def validate_car(cars):
        is_valid = True
        if len(cars['make']) < 3:
            flash('Enter Make of Car!')
            is_valid = False
        if len(cars['model']) < 3:
            flash('Enter Model of Car!')
            is_valid = False
        if len(cars['car_description']) < 3:
            flash('Tell us more about your car!')
            is_valid = False
        return is_valid
