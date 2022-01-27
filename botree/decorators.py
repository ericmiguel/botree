from botree import models
from pydantic import parse_obj_as


def shorten_response(response_key: str):
    def wrapper(func):
        def wrapped(*args, **kwds):
            result = func(*args, **kwds)

            if "shorten" in kwds and kwds["shorten"]:
                result = result[response_key]
            else:
                result["ResponseMetadata"] = parse_obj_as(
                    models.ResponseMetadata, result["ResponseMetadata"]
                )

            return result

        return wrapped

    return wrapper
