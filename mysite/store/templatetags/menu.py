from django import template
from store.models import Category

register = template.Library()


@register.inclusion_tag('store/menu_tpl.html')
def show_menu(dropdown_menu='menu'):
    categories = Category.objects.all()
    return {"categories": categories, "dropdown_menu": dropdown_menu}