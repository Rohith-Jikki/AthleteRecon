from datetime import date
from base64 import b64decode


def null_or_value(value):
    if value == " " or value == "" or value == None:
        return "null"
    return value


def calculateAge(birthDate):
    birthDate = date(*list(map(int, birthDate.split("-"))))
    today = date.today()
    age = today.year - birthDate.year - \
        ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


def image_maker(image, content_type):
    return 'data:' + content_type + ';base64,' + image.decode('utf-8')
