import re
from wtforms import ValidationError

def validate_lowercase(form, field):
    """Custom validator for lowercase letters"""
    r = re.findall("[a-z]", field.data)
    if len(r) == 0:
        raise ValidationError('Must have lowercase letter')

def validate_uppercase(form, field):
    """Custom validator for uppercase letters"""
    r = re.findall("[A-Z]", field.data)
    if len(r) == 0:
        raise ValidationError('Must have uppercase letter')

def special_character(form, field):
    """Custom validator for special characters"""
    r = re.findall('''[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]''', field.data)
    if len(r) == 0:
        raise ValidationError('Must have special character')
