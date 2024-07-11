from app.utils.try_int import try_int


def decode_room(name):
    dictionary = {}
    p_idx = 0
    a_idx = name.index('a')
    dictionary['page'] = try_int(name[p_idx:a_idx], 0)
    if 'd' in name:
        d_idx = name.index('d')
        dictionary['amount'] = try_int(name[a_idx:d_idx], 12)
        dictionary['department_id'] = try_int(name[d_idx:], 1)
        return dictionary
    dictionary['amount'] = try_int(name[a_idx:], 12)
    return dictionary
