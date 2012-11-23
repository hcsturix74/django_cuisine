__author__ = 'Luca'

from django.contrib.admin.util import flatten_fieldsets
from django.forms.models import inlineformset_factory
from django.contrib import admin
from models import *


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'parent')
    inlines = [CategoryInline]


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_type')
    list_filter = ('food_type',)
    search_fields = ('name',)


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 3


class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_name', 'code',)


class GrapeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'region',)
    list_filter = ('name', 'region',)


class WineAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'alcohol_percentage', )
    list_filter = ('year', 'name', 'alcohol_percentage', )
    filter_horizontal = ('grape_type', )


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'alcohol_percentage',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'preparation_time',)
    fields = ('title', 'category', 'summary', 'preparation_time',)
    list_filter = ('title',)
    search_fields = ('title',)
    save_on_top = True
    model = Recipe
    inlines = [IngredientInline, RecipeStepInline, ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodType)
admin.site.register(Food, FoodAdmin)
#admin.site.register(Photo)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Wine, WineAdmin)
admin.site.register(GrapeType, GrapeTypeAdmin)
admin.site.register(Unit, UnitAdmin)
