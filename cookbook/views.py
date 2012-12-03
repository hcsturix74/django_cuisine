# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cookbook.models import Recipe
import datetime

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
        render_to_response(render_to_response("recipe_detail.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request)))
    except Recipe.MultipleObjectsReturned:
        print 'Error, more than one found'
        render_to_response(render_to_response("recipe_detail.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request)))
    new_time = datetime.datetime.now()
    #modify object attributes first
    recipe_obj.created = new_time
    recipe_obj.updated = new_time
    recipe_obj.author = request.user
    recipe_obj.fork_origin = recipe_obj.id
    #set pk to None will save automatically another recipe instance
    recipe_obj.pk = None
    new_recipe = recipe_obj.save()
    #now save recipe steps too, then for Ingredients
    step_list = Recipe.recipestep_set.all()
    new_step_list = map(clone_element, step_list, [new_recipe for new_recipe in len(step_list)])
    ingredient_list = Recipe.ingredient_set.all()
    new_ingredient_list = map(clone_element, ingredient_list, [new_recipe for new_recipe in len(ingredient_list)])
    return render_to_response(render_to_response("recipe_detail.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request)))


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
        return render_to_response(render_to_response("author_recipe_list.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request)))
    else:
        return render_to_response(render_to_response("delete_recipe_error.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request)))
