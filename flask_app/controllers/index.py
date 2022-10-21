from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.users import Users
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template ('home_page.html')

@app.route('/register')
def register():

    return render_template('index.html')

@app.route('/register/user', methods=['POST'])
def register_user():
    if not Users.validate_user(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = Users.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login/valid', methods=['POST'])
def log_val():
    data = {'email': request.form['email']}
    db_user = Users.valid_login(data)
    if not db_user:
        flash('Invalid email or password')
        return redirect('/register')
    if not bcrypt.check_password_hash(db_user.password, request.form['password']):
        flash('Invalid email or password')
        return redirect('/register')
    session['user_id'] = db_user.id
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/home')
def home():
    return render_template('home.html')