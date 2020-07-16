import hashlib
import os

from django.conf import settings


def generate_pin(length=9):
    hash_algorithm = 'sha512'
    m = getattr(hashlib, hash_algorithm)()
    m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
    m.update(os.urandom(16))
    pin = str(int(m.hexdigest(), 16))[-length:]
    return pin