from datetime import date, datetime


def null_or_value(value):
    if value in ['', " ", None]:
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


def inbox_message(name, Id, description, code):
    return {
        name: Id,
        "description": description,
        'date': f'{date.today()}',
        'referral': code
    }


def referral_code_generator(name):
    return f'{name[8:]}{datetime.now().strftime("%H:%M:%S")}{date.today()}'
