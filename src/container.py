import apsw
import handlers
import services
import starlette.applications
import starlette.routing
from functools import cached_property
from apywire.runtime import CompiledAio

class Compiled:

    def db(self):
        if not hasattr(self, '_db'):
            self._db = apsw.Connection(filename='db.sqlite')
        return self._db

    def home_handler(self):
        if not hasattr(self, '_home_handler'):
            self._home_handler = handlers.HomeHandler()
        return self._home_handler

    def users(self):
        if not hasattr(self, '_users'):
            self._users = services.UserService(db=self.db())
        return self._users

    def migrations(self):
        if not hasattr(self, '_migrations'):
            self._migrations = services.MigrationService(db=self.db())
        return self._migrations

    def hello_route(self):
        if not hasattr(self, '_hello_route'):
            self._hello_route = starlette.routing.Route(path='/', endpoint=self.home_handler())
        return self._hello_route

    def user_handler(self):
        if not hasattr(self, '_user_handler'):
            self._user_handler = handlers.UserHandler(users=self.aio.users)
        return self._user_handler

    def user_route(self):
        if not hasattr(self, '_user_route'):
            self._user_route = starlette.routing.Route(path='/users/{screen_name}', endpoint=self.user_handler(), methods=['GET'])
        return self._user_route

    def app(self):
        if not hasattr(self, '_app'):
            self._app = starlette.applications.Starlette(routes=[self.user_route(), self.hello_route()])
        return self._app

    @cached_property
    def aio(self):
        return CompiledAio(self)
compiled = Compiled()