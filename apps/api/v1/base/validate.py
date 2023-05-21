import re
import os
from datetime import datetime
from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    uzbek_regex = r'^\+998\d{9}$'
    validate = re.match(uzbek_regex, value)
    if not validate:
        raise ValidationError(_('Invalid phone number format! Phone number must be uzbek number! +998 XX XXX XX XX'))

    return value


def validate_email(value):
    email_regex = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
    validate = re.match(email_regex, value)
    if not validate:
        raise ValidationError(_("Enter a valid email address"))

    return value


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # File extension
    valid_extensions = ['.png', '.jpg', '.svg', '.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('You can only upload files in jpg, png, svg, .mp4 formats.'))
    return value


def validate_file_size(value):
    file_size = value.size
    if file_size > 10485760:
        raise ValidationError(_("The maximum file size that can be uploaded is 50MB"))
    return value


def validate_datetime(value):
    if value:
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError as e:
            pass
    return False
