import time
import asyncio
from functools import wraps
from pyrogram.types import Message
from typing import Dict

# In-memory storage for last command execution time per user
# user_id -> last_execution_time
last_command_time: Dict[int, float] = {}

def debounce(wait_seconds: float = 1.0):
    """
    Decorator that prevents a user from executing a command too rapidly.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message, *args, **kwargs):
            if not isinstance(message, Message) or not message.from_user:
                return await func(client, message, *args, **kwargs)

            user_id = message.from_user.id
            current_time = time.time()

            last_time = last_command_time.get(user_id, 0)
            if current_time - last_time < wait_seconds:
                # Optional: Send a warning or just ignore
                return

            last_command_time[user_id] = current_time
            return await func(client, message, *args, **kwargs)
        return wrapper
    return decorator
