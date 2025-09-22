from django import template
from apps.site_config.models import SiteSettings
import re

register = template.Library()

@register.simple_tag
def get_site_settings():
    return SiteSettings.objects.first()

@register.filter
def only_digits(value):
    return re.sub(r'\D', '', str(value))