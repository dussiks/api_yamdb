import datetime
from django.core.exceptions import ValidationError


def year_validator(value):
    if value < 1900 or value > datetime.datetime.now().year:
        raise ValidationError(
            ' Год %(value)s ввведен неверно.',
            params={'value': value},
        )
