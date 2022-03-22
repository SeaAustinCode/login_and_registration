from flask_app import app
from flask import render_template, redirect, session, request

from flask_app.models.model_user import User

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    user = User.get_one({"id":session["uuid"]}) #variable user = class(User)function to select(give it the value of the user that is logged in)
    return render_template('dashboard.html', user=user)