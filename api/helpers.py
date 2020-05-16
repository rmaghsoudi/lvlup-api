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

# leveling formula
def xp_to_lvlup(level):
    xp_needed = 5 * (level ^ 2) + 500 * level + 1000
    return xp_needed


def will_lvlup(data, user):
    user_copy = {'level': user.level, 'xp': user.xp,
                 'auth_id': user.auth_id, 'id': user.id}
    xp_to_add = int(data['xp'])
    xp_needed = xp_to_lvlup(user.level)
    new_xp = user.xp + xp_to_add

    if new_xp >= xp_needed:
        user_copy['level'] += 1
        user_copy['xp'] = new_xp
    else:
        user_copy['xp'] = new_xp

    return user_copy
