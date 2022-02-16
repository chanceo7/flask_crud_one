from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user_model import User
from flask_app.controllers import magazin
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def landing_page():
    return render_template("index.html")
    
@app.route('/sign', methods=['POST'])
def sign_in():

    if not User.form_checker(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    user=User.insert_user(data)
    if not user:
        flash('this email already exist')
        return redirect('/')
    return redirect('/')



@app.route('/login', methods=['POST'])
def login():
    data={
        'email':request.form['email']
    }

    user_data=User.get_by_email(data)

    if user_data==False:
        flash('user/email invalid')
        return redirect('/')

    if bcrypt.check_password_hash(user_data.password, request.form["password"])== False:
        flash("Invalid Email/Password")
        return redirect("/")
    session['user_id']=user_data.id
    session['first_name']=user_data.first_name
    session['last_name']=user_data.last_name
    session['email']=user_data.email
    return redirect('/dashboard')


@app.route('/update' , methods=['POST'])
def update(): 

    if not User.update_checker(request.form):
        return redirect('/account')

    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'id':session['user_id']
    }
    User.update(data)
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    return redirect('/dashboard')


@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!")
    return redirect("/")
