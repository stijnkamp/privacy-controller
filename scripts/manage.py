from werkzeug.security import generate_password_hash
from flask_script import Manager
from os.path import dirname, abspath
import sys
import utils
import web
import web.auth.models as auth_models
from resolver.resolver_commands import ResolverCommands

p = dirname(dirname(abspath(__file__)))
sys.path.insert(1, p)

manager = Manager(web.app)

@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
@manager.option('-n', '--name', dest='name', default='User')
def add_user(email, password, name):
    """the function saves the password into the config file using the config class"""
    if(email and password and name):
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = auth_models.User(email=email, name=name, password=hashed_password)
        web.db.session.add(new_user)
        web.db.session.commit()
        utils.log('Successfully added user {}'.format(email))
    else:
        utils.log('Email, password and name are needed')

@manager.command
def check_sources():
    """the function saves the password into the config file using the config class"""
    resolver = ResolverCommands()
    resolver.check_all_sources()


if __name__ == "__main__":
    manager.run()
