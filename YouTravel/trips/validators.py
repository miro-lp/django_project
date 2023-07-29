from django.core.exceptions import ValidationError


def is_title_start_alpha(title):
    if not title[0].isalpha():
        raise ValidationError('Title must start with alphabet letter')


def is_title_start_capitalized(title):
    if not title[0].isupper():
        raise ValidationError('Title must start with capitalized letter')


def is_title_length_less(title):
    if len(title) < 4:
        raise ValidationError('Title must have more than 3 symbols')
