import web.auth.models
import werkzeug.security
import web
import flask_script import Manager
import os.path import dirname, abspath
import sys
import utils
p = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.insert(1, p)
manager = flask_script.Manager(app)


@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
@manager.option('-n', '--name', dest='name', default='User')
def add_user(email, password, name):
    """the function saves the password into the config file using the config class"""
    if(email and password and name):
        hashed_password = security.generate_password_hash(password, method='sha256')

        new_user = models.User(email=email, name=name, password=hashed_password)
        web.db.session.add(new_user)
        web.db.session.commit()
        utils.log('Successfully added user {}'.format(email))
    else:
        utils.log('Email, password and name are needed')


if __name__ == "__main__":
    manager.run()
