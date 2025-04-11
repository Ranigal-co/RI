from ..models import Project
from app.extensions import db


def getProjects(page: int, count=3):
    """Page - страница\nCount - количество получаемых проектов\nВозвращает список объектов"""
    output = list()
    length = Project.query.count()

    first_index = page * count
    for index in range(first_index, first_index + count):
        if index < length:
            values = Project.query.get(index + 1).to_dict()
            output.append(values)
        else:
            break
    return output
