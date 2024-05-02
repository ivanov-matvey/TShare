import string
import random


def generate_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
