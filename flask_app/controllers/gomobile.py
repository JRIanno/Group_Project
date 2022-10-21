from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.users import Users
from flask_app.models.clubs import Carmeets
from flask_app.models.rides import Cars

@app.route('/new/car')
def new_car():
    if 'user_id' not in session:
        return redirect('/register')
    data = {
        'id': session['user_id'],
    }
    return render_template('car_dashboard.html', users = Users.get_id(data), cars = Cars.get_all_cars(data))


@app.route('/new/car/add', methods=['POST'])
def add_car():
    if 'user_id' not in session:
        return redirect('/register')
    data = {
        'user_id': request.form['user_id'],
        'make': request.form['make'],
        'model': request.form['model'],
        'car_description': request.form['car_description'],
    }

    Cars.share_car(data)
    return redirect('/new/car')


@app.route('/show/<int:car_id>/car')
def single_car(car_id):
    data = {
        'id': id,
        'id': session['user_id'],
    }
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('car_show.html', users = Users.get_id(data), cars = Cars.one_car(car_id))

@app.route('/update_car/<int:car_id>')
def update_car(car_id):
    data = { 'id': session['user_id']}
    return render_template('car_update.html',users = Users.get_id(data), cars = Cars.one_car(car_id))

@app.route('/edit/<int:car_id>', methods = ['POST'])
def edit_car(car_id):
    data = {
        'id': request.form['id'],
        'make': request.form['make'],
        'model': request.form['model'],
        'car_description': request.form['car_description'],
    }
    if 'user_id' not in session:
        return redirect('/')
    Cars.update_car(data)
    return redirect('/new/car')


@app.route('/<int:car_id>/delete')
def delete_car(car_id):
    Cars.delete_car(car_id)
    return redirect('/new/car')