from functools import wraps
import time
from pyrogram.types import Message, CallbackQuery

def debounce(wait):
    """Decorator that will postpone a functions execution until after wait seconds
    have elapsed since the last time it was invoked."""
    def decorator(fn):
        last_called = {}
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            # Try to get user_id from Message or CallbackQuery
            user_id = None
            for arg in args:
                if isinstance(arg, (Message, CallbackQuery)):
                    user_id = arg.from_user.id
                    break

            if user_id:
                now = time.time()
                if user_id in last_called and now - last_called[user_id] < wait:
                    return
                last_called[user_id] = now
            return await fn(*args, **kwargs)
        return wrapper
    return decorator
