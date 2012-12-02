__author__ = 'luca'
from cookbook.models import Recipe, Category
from django import template
import settings
from django.utils.safestring import mark_safe


register = template.Library()

@register.inclusion_tag('')
def show_recipes_by_category(category_id):
    """visualize example charts"""

    rec_list = Recipe.objects.filter(category=category_id)
    cat = Category.objects.get(id=category_id)
    return {'recipe_list':rec_list ,
            'category' : cat,
    }





@register.inclusion_tag('tt_veg_friendly.html')
def show_vegetarian_recipes():
    """
    This tag shows the list of vegetarian recipes
    """

    rec_list = Recipe.veg_objects.vegetarian_friendly()
    return {'recipe_list':rec_list ,
            }


@register.inclusion_tag('tt_veg_friendly.html')
def show_vegan_recipes():
    """
    This tag shows the list of vegan recipes
    """
    rec_list = Recipe.veg_objects.vegan_friendly()
    return {'recipe_list':rec_list ,
            }


@register.simple_tag(name='get_forks_count')
def show_forks_count(value):
    """
    This tag shows the number of fork for a given one
    """
    return Recipe.objects.filter(fork_origin=value).count()


@register.simple_tag(name='get_recipes_count_per_user')
def show_recipes_count_per_user(value):
    """
    This tags shows the number of recipes for a given user
    """
    return Recipe.objects.filter(author=value).count()

