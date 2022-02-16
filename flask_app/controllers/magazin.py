import re
from flask_app import app
from flask_app.models.magazin_model import Magazin
from flask import redirect, session, request,render_template,flash

@app.route('/dashboard')
def dashbord(): 
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect('/')

    data=Magazin.get_magazines()
    return render_template('dashboard.html', datas=data)


@app.route('/show/<int:id>')
def show(id):
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect('/')
    data={
        'id':id
    }
    datas=Magazin.get_details(data)
    return render_template('show.html', data=datas)

@app.route('/add')
def add():
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect('/')
    return render_template('add.html')


@app.route('/insert', methods=['POST'])
def insert():
    
    if not Magazin.magazine_checker(request.form):
        return redirect('/add')

    data={
        'name':request.form['name'],
        'description':request.form['description'],
        'user_id':session['user_id']
    }
    Magazin.insert(data)
    return redirect ('/dashboard')


@app.route('/account')
def account():
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    datas = Magazin.user_magazine(data)
    return render_template('account.html', datas=datas)


@app.route('/delete/<int:id>')
def delete(id):
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect('/')
    data={
        'id':id
    }
    Magazin.delete(data)
    return redirect('/account')