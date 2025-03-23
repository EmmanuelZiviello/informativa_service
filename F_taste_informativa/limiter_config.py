
# to block many request in login 
from flask import current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter( key_func=get_remote_address)

def set_limiter_config():
    if current_app.config["REDIS_PASSWORD"] is not None:
        limiter = Limiter(
        app=None,
        key_func=get_remote_address,
        storage_uri="redis://:" + current_app.config["REDIS_PASSWORD"] + "@" + current_app.config["REDIS_HOST"] + ":" + str(current_app.config["REDIS_PORT"]),
        storage_options={"socket_connect_timeout": 30},
        strategy="fixed-window",  # or "moving-window"
        )
    else:
        limiter = Limiter(
        app=None,
        key_func=get_remote_address,
        storage_uri="redis://" + current_app.config["REDIS_HOST"] + ":" + str(current_app.config["REDIS_PORT"]),
        storage_options={"socket_connect_timeout": 30},
        strategy="fixed-window",  # or "moving-window"
        )
    
def get_limiter():
    return limiter