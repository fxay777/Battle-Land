import datetime

from django import template
from users.lib import *

register = template.Library()

@register.filter
def get_faction_size(faction):
    return len(faction['coleaders']) + len(faction['officers']) + len(faction['members']) + 1
