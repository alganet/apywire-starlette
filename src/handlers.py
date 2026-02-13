# SPDX-FileCopyrightText: 2026 Alexandre Gomes Gaigalas <alganet@gmail.com>
#
# SPDX-License-Identifier: ISC

from starlette.responses import JSONResponse
from starlette.requests import Request
import services


class UserHandler:
    def __init__(self, users: services.UserService):
        self.users = users

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)
        screen_name = request.path_params["screen_name"]
        user = self.users.get_user(screen_name)
        if user:
            await JSONResponse({"user": user})(scope, receive, send)
        else:
            await JSONResponse({"error": "User not found"}, status_code=404)(
                scope, receive, send
            )


class HomeHandler:
    async def __call__(self, scope, receive, send):
        await JSONResponse({"message": "Hello World!"})(scope, receive, send)
