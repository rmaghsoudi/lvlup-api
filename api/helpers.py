from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

types = {'task': 1, 'pillar': 5, 'goal': 10}


def validate_type(value):
    if value not in types.keys():
        raise ValidationError(
            _('%(value)s is not an entry type'),
            params={'value': value},
        )


def calculate_xp(req_data):
    new_data = req_data.copy()
    multiplier = types[req_data['type']]
    xp = (100 * int(req_data['difficulty'])) * multiplier
    new_data['xp'] = xp
    return new_data

