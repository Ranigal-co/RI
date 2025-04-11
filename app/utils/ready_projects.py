from ..models import Project
from app.extensions import db


def registry():
    """
        Регистрация проектов в базу данных
    """

    projects = list()
    projects.append({"title": "PYQT1",
                     "description": "Наш первый проект по Яндекс.Лицей",
                     "link": "0"})
    projects.append({"title": "PYQT2",
                     "description": "fgеногртпиауцйпкреиавперотпиавкпернорьтпиавапкероьтавапкерноьтпавупкретопимавапрть имапаптрьopeporg",
                     "link": "1"})
    projects.append({"title": "PYQT3",
                     "description": "123325234",
                     "link": "2"})
    projects.append({"title": "PYQT4",
                     "description": "Наш первый проектqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
                     "link": "3"})

    for params in projects:
        project = Project(title=params["title"],
                          description=params["description"],
                          link=params["link"])
        db.session.add(project)
    db.session.commit()


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
