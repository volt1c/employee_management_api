import re


def validate_room(name):
    pattern = re.compile("^b[0-9]+a[0-9]+(d[0-9]+)?$")
    if pattern.match(name):
        return True
    return False
