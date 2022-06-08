
from flask import request, send_from_directory, redirect
import utils
import config
import thread

from web import app
from web.api import Api
from web.auth import Auth

# Register the general application
@app.route('/docs')
def docs_redirect():
    return redirect("/docs/index.html", code=302)

@app.route('/docs/<path:file>')
def docs(file):
    return send_from_directory('../docs/build/html', file)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")


class WebServer(thread.Thread):
    """A Flask webserver serving the static frontend and provides a REST Api. 

    Args:
        state (State): The shared state with other services
    """
    def __init__(self, state):
        super().__init__('Webserver', state)
        self.setup_modules()

    def setup_modules(self):
        """Register the different classfull Flask modules
        """
        modules = [Api(self.state), Auth(self.state)]
        for module in modules:
            module.register(app)

    def _monitor(self):
        utils.safe_run(
            app.run, kwargs={'port': config.flask['PORT'], 'host': config.flask['HOST']})
