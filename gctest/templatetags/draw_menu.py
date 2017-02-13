from django import template

from ..tree_getter import get_tree


register = template.Library()

@register.inclusion_tag('main.html', takes_context=True)
def draw_menu(context, menu_name):
    return get_tree(menu_name, context['request'].path)