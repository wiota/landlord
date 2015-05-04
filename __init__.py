from threading import Lock


class Landlord(object):

    def __init__(self, create_app, subdomains=[]):
        """ Initialize the application dispatcher. """

        # The function to call when creating a new app
        self.create_app = create_app

        # Threading lock
        self.lock = Lock()

        # Instances of already created applications
        self.instances = {}

        # Subdomains to strip out of the domain
        self.subdomains = subdomains

    def get_application(self, host, subdomains=[]):
        """ Return an initialized application for a given host. """

        # Extract the hostname from the port
        host = host.split(':')[0]

        # Strip the subdomains from the hostname
        for subdomain in self.subdomains:
            host = host.replace('{}.'.format(subdomain), '')

        with self.lock:
            # Get the correct app from the instances list
            app = self.instances.get(host)

            # If the app doesn't already exist, create it
            if app is None:
                app = self.create_app(host)

                # Add it to the instances list
                self.instances[host] = app
            return app

    def __call__(self, environ, start_response):
        app = self.get_application(environ['HTTP_HOST'])
        return app(environ, start_response)
