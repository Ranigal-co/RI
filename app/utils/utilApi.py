from ..models import ApiKey
from app.extensions import db

def get(page: int, count=3):
    """Page - страница\nCount - количество получаемых проектов\nВозвращает список объектов"""
    output = list()
    length = ApiKey.query.count()

    first_index = page * count
    for index in range(first_index, first_index + count):
        if index < length:
            values = ApiKey.query.get(index + 1).to_dict()
            output.append(values)
        else:
            break
    return output
