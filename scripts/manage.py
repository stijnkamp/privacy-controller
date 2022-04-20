from os.path import dirname, abspath
import sys
p = dirname(dirname(abspath(__file__)))
sys.path.insert(1, p)
from flask_script import Manager
from web import app, db
from werkzeug.security import generate_password_hash
from web.auth.models import User
manager = Manager(app)

@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
@manager.option('-n', '--name', dest='name', default='User')
def add_user(email, password, name):
    """the function saves the password into the config file using the config class"""
    if(email and password and name):
        hashed_password = generate_password_hash(password, method='sha256')
        
        new_user = User(email=email, name=name, password=hashed_password)
        db.session.add(new_user) 
        db.session.commit()   
        print('Successfully added ', email)
    else:
        print('Email, password and names are needed')
        
if __name__ == "__main__":
    manager.run()