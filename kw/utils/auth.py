from functools import wraps

import jwt
from sanic import text

def check_token(request):
    # return True
    token = request.headers.get("authorization", False)
    if len(token.split(" ")[1]) < 2:
        return False
    token = token.split(" ")[1]
    
    try:
        data = jwt.decode(
            token, request.app.config.SECRET, algorithms=["HS256"]
        )
        if data.get('login') == 'True':     return True
    except jwt.exceptions.InvalidTokenError:
        return False
    except:
        return False

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)