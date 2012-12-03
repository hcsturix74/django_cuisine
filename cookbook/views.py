# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cookbook.forms import FrontendRecipeEditForm
from cookbook.models import Recipe, Ingredient, RecipeStep
import datetime
import cookbook_settings

def homepage(request):
    """
    Just a simple homepage
    """
    return render_to_response("homepage.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request))



def clone_element(el, pkval):
    """
    utility function: clone an object and save it, setting
    its foreign key to pkval.
    It's used for:
    - RecipeIngredient
    - RecipeStep
    """
    new_time = datetime.datetime.now()
    el.created = new_time
    el.updated = new_time
    el.recipe = pkval
    el.pk = None
    return el.save()

@login_required
def fork_recipe(request, recipe_id):
    """
    This is a view to fork a Recipe with its steps and ingredients
    """
    try:
        recipe_obj = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        print 'Error, This Recipe does not exist'
        return render_to_response("recipe_detail.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request))
    except Recipe.MultipleObjectsReturned:
        print 'Error, more than one found'
        return render_to_response("recipe_detail.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request))
    new_time = datetime.datetime.now()
    #modify object attributes first
    recipe_obj.created = new_time
    recipe_obj.updated = new_time
    recipe_obj.author = request.user
    recipe_obj.fork_origin = recipe_obj.id
    #set pk to None will save automatically another recipe instance
    recipe_obj.pk = None
    recipe_obj.save()
    #now save recipe steps too, then for Ingredients
    step_list = Recipe.recipestep_set.all()
    new_step_list = map(clone_element, step_list, [recipe_obj for recipe_obj in len(step_list)])
    ingredient_list = Recipe.ingredient_set.all()
    new_ingredient_list = map(clone_element, ingredient_list, [recipe_obj for recipe_obj in len(ingredient_list)])
    return render_to_response("recipe_detail.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request))


@login_required
def delete_recipe(request, recipe_id):
    """
    This is a view to delete an existing recipe.
    Users can only deleet their own recipes
    """
    try:
        recipe_obj = Recipe.objects.get(i=recipe_id)
    except Recipe.DoesNotExist:
        pass
    except Recipe.MultipleObjectsReturned:
        pass
    if request.user == recipe_obj.author:
        recipe_obj.delete()
        return render_to_response("author_recipe_list.htm", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request))
    else:
        #Change it into a HttpRedirect? Later on yes...
        return render_to_response("delete_recipe_error.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request))



@login_required
def create_recipe(request):
    """
    This view manages a recipe creation
    It is the same as in Admin, so we use inline-dynamic-formset
    request  - the HTTP request coming from the user
    return   - renders a template
    """
    user = request.user
    IngredientInlineFormSet = inlineformset_factory(Recipe, Ingredient,
                                                    extra = cookbook_settings.DJANGO_CUISINE_INGREDIENT_EXTRA,
                                                    max_num=cookbook_settings.DJANGO_CUISINE_INGREDIENT_MAX_NUM,
                                                    can_delete=True)
    RecipeStepInlineFormSet = inlineformset_factory(Recipe, RecipeStep,
                                                    extra = cookbook_settings.DJANGO_CUISINE_RECIPE_STEPS_EXTRA,
                                                    max_num=cookbook_settings.DJANGO_CUISINE_RECIPE_STEPS_MAX_NUM,
                                                    can_delete=True)

    #Post method
    if request.method == "POST":
        edit_form = FrontendRecipeEditForm(request.POST, instance=user)
        ingredient_formset = IngredientInlineFormSet(request.POST, request.FILES, instance=user, prefix='ingredient')
        recipe_step_formset = RecipeStepInlineFormSet(request.POST, request.FILES, instance=user, prefix='recipestep')
        if edit_form.is_valid() and ingredient_formset.is_valid() and  recipe_step_formset.is_valid():
            edit_form.save()
            ingredient_formset.save()
            recipe_step_formset.save()
            # Do something. Should generally end with a redirect. For example:
            #TODO: Modify this to render the correct URL
            return HttpResponseRedirect(reverse('user-recipe-list', args=(user.id,)))
    # this is GET method instead
    else:
        edit_form = FrontendRecipeEditForm(instance=user)
        ingredient_formset = IngredientInlineFormSet(instance=user, prefix='ingredient')
        recipe_step_formset = RecipeStepInlineFormSet(instance=user, prefix='recipestep')
    #TODO: Modify this to render the correct template
    return render_to_response("edit_recipe.html", {
        "edit_form": edit_form,
        "ingredient_formset": ingredient_formset,
        "recipe_step_formset": recipe_step_formset,
        "error_message": edit_form.errors,
        }, context_instance=RequestContext(request))

