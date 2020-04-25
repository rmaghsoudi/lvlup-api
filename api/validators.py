from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

types = ['task', 'pillar', 'goal']

def validate_type(value):
    if value not in types:
        raise ValidationError(
            _('%(value)s is not an entry type'),
            params={'value': value},
        )