from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from redis import ConnectionError


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except ConnectionError:
                return {"message": "Connection error with Redis"}, 500
            except:
                return {"message": "Unauthorized"}, 401
            claims = get_jwt()
            if claims["role"] == 'admin':
                return fn(*args, **kwargs)
            else:
                raise NoAuthorizationException("Admin only!")

        return decorator

    return wrapper

class NoAuthorizationException(Exception):
    pass
#    def __init__(self, message, errors):            
        # Call the base class constructor with the parameters it needs
    #    super().__init__(message)
            
        # Now for your custom code...
    #    self.errors = errors