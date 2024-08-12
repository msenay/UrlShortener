import logging

import redis
import json

from app.database.models import URL
from app.settings import settings

# Configure Redis
store = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
)

# Cache decorator
logger = logging.getLogger(__name__)


# Cache decorator with logging
def cache_result(key_prefix, expiration_seconds=30):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            # Generate the cache key without including the session object
            key_parts = [key_prefix] + [v for k, v in kwargs.items() if k != "db_session"]
            key = "-".join(str(k) for k in key_parts)
            result = store.get(key)

            if result is None:
                # Call the original function and cache its result
                value = func(*args, **kwargs)

                # Convert SQLAlchemy object to a dictionary (serializable format)
                if value:
                    value_dict = {c.name: getattr(value, c.name) for c in value.__table__.columns}
                    value_json = json.dumps(value_dict)
                    store.setex(key, expiration_seconds, value_json)
            else:
                # Decode the cached result from bytes to a string and then to a dictionary
                value_json = result.decode("utf-8")
                value_dict = json.loads(value_json)
                # Convert the dictionary back to a URL instance
                value = URL(**value_dict)

            return value

        return wrapped

    return wrapper
