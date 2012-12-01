__author__ = 'Luca'

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
    list_display = ('name', 'origin',)
    list_filter = ('name', 'origin',)


class WineAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'alcohol_percentage', )
    list_filter = ('year', 'name', 'alcohol_percentage', )
    filter_horizontal = ('grape_type', )


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3

class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'country',)
    list_editable = ('country', )
    list_filter = ('country', )

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent',)
    list_filter = ('continent', )


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'alcohol_percentage',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'preparation_time', 'is_for_vegan', 'is_for_vegetarian',)
    list_filter = ('title', 'is_for_vegan', 'is_for_vegetarian', )
    search_fields = ('title',)
    filter_horizontal = ('suggested_wine', )
    save_on_top = True
    model = Recipe
    inlines = [IngredientInline, RecipeStepInline, ]

    def save_model(self, request, obj, form, change):
        """
        This method overrides the default one
        We save the current user putting it as author
        """
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()



admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodType)
admin.site.register(Food, FoodAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Wine, WineAdmin)
admin.site.register(GrapeType, GrapeTypeAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Unit, UnitAdmin)
