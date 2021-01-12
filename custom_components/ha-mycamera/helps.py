from homeassistant.exceptions import HomeAssistantError
from typing import Any, Callable, List, Text

def retry_async(limit: int = 5,
                delay: float = 1,
                catch_exceptions: bool = True
                ) -> Callable:
    """Wrap function with retry logic.
    The function will retry until true or the limit is reached. It will delay
    for the period of time specified exponentialy increasing the delay.
    Parameters
    ----------
    limit : int
        The max number of retries.
    delay : float
        The delay in seconds between retries.
    catch_exceptions : bool
        Whether exceptions should be caught and treated as failures or thrown.
    Returns
    -------
    def
        Wrapped function.
    """
    def wrap(func) -> Callable:
        import functools
        import asyncio
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            _LOGGER.debug(
                "%s.%s: Trying with limit %s delay %s catch_exceptions %s",
                func.__module__[func.__module__.find('.')+1:],
                func.__name__,
                limit,
                delay,
                catch_exceptions)
            retries: int = 0
            result: bool = False
            next_try: int = 0
            while (not result and retries < limit):
                if retries != 0:
                    next_try = delay * 2 ** retries
                    await asyncio.sleep(next_try)
                retries += 1
                try:
                    result = await func(*args, **kwargs)
                except Exception as ex:  # pylint: disable=broad-except
                    if not catch_exceptions:
                        raise
                    template = ("An exception of type {0} occurred."
                                " Arguments:\n{1!r}")
                    message = template.format(type(ex).__name__, ex.args)
                    _LOGGER.debug(
                        "%s.%s: failure caught due to exception: %s",
                        func.__module__[func.__module__.find('.')+1:],
                        func.__name__,
                        message)
                _LOGGER.debug(
                    "%s.%s: Try: %s/%s after waiting %s seconds result: %s",
                    func.__module__[func.__module__.find('.')+1:],
                    func.__name__,
                    retries,
                    limit,
                    next_try,
                    result
                    )
            return result
        return wrapper
    return 
