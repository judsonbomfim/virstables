from django import template

register = template.Library()

@register.filter
def foto_destaque(fotos):
    return fotos.filter(is_destaque=True).first()