"""
Idempotent API for managing users
"""
from fabtools.user import *


def user(name):
    """
    I can haz user
    """
    if not exists(name):
        create(name)
