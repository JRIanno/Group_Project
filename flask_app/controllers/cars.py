from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.users import Users
from flask_app.models.clubs import Carmeets

@app.route('/dashboard')
def user_dash():
    if 'user_id' not in session:
        return redirect('/register')
    data = { 'id': session['user_id']}
    return render_template('profile_dashboard.html',users = Users.get_follow(data))

@app.route('/dashboard/create', methods=['POST'])
def user_create():
    data = { 
        'creator_id': request.form['creator_id'],
        'name': request.form['name'],
        'type': request.form['type'],
        'location': request.form['location'],
        'date_time': request.form['date_time'],
    }
    if 'user_id' not in session:
        return redirect('/')
    Carmeets.create_meet(data)
    return redirect('/dashboard')



@app.route('/pick/<int:carmeets_id>')
def pick(carmeets_id):
    data = {
        'id': id,
        'id': session['user_id'],
    }
    if 'user_id' not in session:
        return redirect('/register')
    return render_template('show_club.html', users = Users.get_id(data), carmeets = Carmeets.meet_up(carmeets_id))

@app.route('/following', methods=['POST'])
def following():
    data = {
        'follow_id': request.form['follow_id'],
        'meet_id': request.form['meet_id'],
    }
    if 'user_id' not in session:
        return redirect('/')
    Carmeets.follow(data)
    return redirect('/dashboard')

@app.route('/club/dash')
def club_dash():
    data = {
        'id': session['user_id']
    }
    if 'user_id' not in session:
        return redirect('/register')
    return render_template('club_dashboard.html', users = Users.get_id(data), carmeets = Carmeets.get_club_id())

@app.route('/club/<int:carmeets_id>')
def club_edit(carmeets_id):
    data = {
        'id': id,
        'id': session['user_id'],
    }
    if 'user_id' not in session:
        return redirect('/register')
    return render_template('update.html', users = Users.get_id(data), carmeets = Carmeets.meet_up(carmeets_id))


@app.route('/update/<int:carmeets_id>', methods=['POST'])
def edit(carmeets_id):
    data = { 
        'id': request.form['id'],
        'creator_id': request.form['creator_id'],
        'name': request.form['name'],
        'type': request.form['type'],
        'location': request.form['location'],
        'date_time': request.form['date_time'],
    }
    if 'user_id' not in session:
        return redirect('/')
    Carmeets.update(data)
    return redirect(f'/pick/{carmeets_id}')

@app.route('/delete/<int:carmeets_id>')
def delete_meet(carmeets_id):
    Carmeets.delete(carmeets_id)
    return redirect('/club/dash')
