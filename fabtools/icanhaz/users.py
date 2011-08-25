"""
Idempotent API for managing users
"""
from fabtools.users import *


def user(name):
    """
    I can haz user
    """
    if not user_exists(name):
        create_user(name)
