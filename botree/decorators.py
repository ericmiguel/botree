"""Botree Decorators."""

from typing import Callable


def shorten_response(response_key: str) -> Callable:
    """
    Trim the metadata from the AWS API response.

    Only serves to the purpose of a cleaner response.

    Parameters
    ----------
    response_key : str
        Each AWS response has a different response key. For example:
        AWS Secrets Manager list secrets call has a "SecretList" key containing
        all the existing secrets.

    Returns
    -------
    Callable
        decorated function without metadata.
    """

    def wrapper(func):
        def wrapped(*args, **kwds):
            result = func(*args, **kwds)

            if "shorten" in kwds and kwds["shorten"]:
                result = result[response_key]

            return result

        return wrapped

    return wrapper
