from app.utils.try_int import try_int


def encode_room(data: dict):
    name = ''
    page = try_int(data['page'], 0)
    amount = try_int(data['amount'], 12)
    name += f'p{page}'
    name += f'a{amount}'
    if 'department_id' in data:
        department_id = try_int(data['department_id'], None)
        if department_id:
            name += f'd{department_id}'
    return name
