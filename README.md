landlord
========

Landlord lets a single Flask application support multiple tenants, based on the HOSTNAME. One application can return either multiple instances of the same application for every hostname, or a different application per hostname. Landlord will also never ask you for rent.

Brought to you by [wiota.co](http://wiota.co).

## Requirements

Flask, obviously:

    $ pip install flask

## Usage

In your `app.py`:

    from flask import Flask
    from landlord import Landlord
    from your_app import create_app
    
    if __name__ == '__main__' :
        app = Flask(__name__)
        app.wsgi_app = Landlord(create_app)
        app.run()

In your sub-application's `__init__.py`:

    from flask import Flask
    
    def create_app(hostname):
        app = Flask(__name__)
        app.config['HOST'] = hostname
    
        @app.route('/')
        def root():
            return "Currently running on host: %s" % (app.config['HOST'])
    
        return app

## Tips

- If you're running your app on localhost, you should add the relevant hostnames to your `/etc/hosts` file to see the differences
- Best used in conjunction with Flask Blueprints: http://flask.pocoo.org/docs/blueprints/

## License

MIT License.
