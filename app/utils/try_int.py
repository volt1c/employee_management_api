def try_int(string, default):
    try:
        v = int(string)
    except ValueError:
        v = default
    return v
