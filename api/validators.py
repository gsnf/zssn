from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def valida_latitude(lat):
    if lat > 90 or lat < -90:
        raise ValidationError(
            _('Varia de -90 a 90.'),
            params={'lat': lat},
        )

def valida_longitude(lon):
    if lon > 180 or lon < -180:
        raise ValidationError(
            _('Varia de -180 a 180.'),
            params={'lon': lon},
        )
        
def maior_que_zero(num):
    if num < 0:
        raise ValidationError(
            _('Não pode ser menor que zero.'),
            params={'num': num},
        )
