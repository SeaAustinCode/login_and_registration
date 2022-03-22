from flask import Flask 
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "6153e8aa-01a3-4546-b8a0-e5bd57e272a4" #(when using session, good place to get one, powershell new-guid (use that code))
DATABASE = 'login_and_registration_assignment_db'

bcrypt = Bcrypt(app)