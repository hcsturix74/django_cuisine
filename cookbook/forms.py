__author__ = 'luca'
from django.forms import ModelForm
from models import Recipe , Wine

class FrontendRecipeEditForm(ModelForm):

    """
    This is a form created using UserChangeForm contained in django.contrib.auth.forms
    It is used to have UserChnageForm in a revisited way.
    In front-end some parameters should be excluded as they are not confiurable by user but only by admin
    or staff members.
    These parameters (fields) are:
    """

    def __init__(self, *args, **kwargs):
        super(FrontendRecipeEditForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        exclude = ('fork_origin', 'is_published',)


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe

class WineForm(ModelForm):
    class Meta:
        model = Wine



