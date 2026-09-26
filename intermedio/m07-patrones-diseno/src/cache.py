from collections.abc import Callable
from functools import wraps


def cached[**Parameters, Result](
    function: Callable[Parameters, Result],
) -> Callable[Parameters, Result]:
    cache: dict[tuple[object, ...], Result] = {}

    @wraps(function)
    def wrapper(
        *args: Parameters.args,
        **kwargs: Parameters.kwargs,
    ) -> Result:
        key = args + tuple(sorted(kwargs.items()))

        if key not in cache:
            cache[key] = function(*args, **kwargs)

        return cache[key]

    return wrapper
