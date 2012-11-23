from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
import datetime

from managers import VegManager, PublishedManager

#Some choices here
DIFFICULTY_CHOICES = ((1, _('Very Easy')),
                      (2, _('Easy')),
                      (3, _('Medium')),
                      (4, _('Difficult')),
                      (5, _('Very Difficult')),)

#unit type, for Weight, Volume or other....
UNIT_TYPE = ((1, _('Weight')),
             (2, _('Volume')),
             (3, _('Other')),)

#Continent list, used for Country
CONTINENT_LIST = ((1, _('Europe')),
                  (2, _('Asia')),
                  (3, _('Africa')),
                  (4, _('America')),
                  (5, _('Oceania')),)


WINE_KIND_LIST = ((1, _('Red')),
                 (2, _('White')),
                 (3, _('Sparkling')),
                 (4, _('Fortified')),)


class GenericBaseModel(models.Model):
    """
    GenericBaseModel class - inherits from models.Model
    This class is an abstract structure for site
    content (not translatable fields, see GenericBaseTranslationModel) management
    It provides some basic attributes (i.e. table columns) common to Content base
    applications
    """
    is_published = models.BooleanField(blank=True, default=True, verbose_name=_('Published'))
    created = models.DateTimeField(verbose_name=_('Creation Date'), default=datetime.datetime.now())
    updated = models.DateTimeField(verbose_name=_('Modify Date'), default=datetime.datetime.now())
    objects = models.Manager()
    pub_objects = PublishedManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        This is the overridden save method
        """
        if not self.id:
            self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()
        super(GenericBaseModel, self).save(*args, **kwargs)

    def get_history(self):
        """
        This method retrieves the history for this object searching in LogEntry Table
        """
        lst = []
        try:
            lst = LogEntry.objects.filter(content_type=ContentType.objects.get_for_model(self).id, object_id=self.pk)
        except LogEntry.DoesNotExist:
            pass
        return lst

    def _get_creation_date(self):
        """
        This method retrieves the creation date for this object
        """
        return self.created

    creation_date = property(_get_creation_date)

    def _get_modify_date(self):
        """
        This method retrieves the modification date for this object
        """
        return self.updated

    modify_date = property(_get_modify_date)


class Category(GenericBaseModel):
    """
    Category class - inherits from GenericBaseModel
    """
    name = models.CharField(verbose_name=_('Category'), max_length=60, blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name=_('Parent'))
    order = models.IntegerField(verbose_name=_('Order'), blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Country(GenericBaseModel):
    """
    Country class - inherits from GenericBaseModel
    """
    name = models.CharField(verbose_name=_('Country'), max_length=60, blank=True, null=True)
    continent = models.IntegerField(verbose_name=_('Continent'), choices=CONTINENT_LIST)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class GrapeType(GenericBaseModel):
    """
    GrapeType class - inherits from GenericBaseModel
    """

    name = models.CharField(max_length=200, verbose_name=_('Grape Name'))
    region = models.CharField(max_length=200, verbose_name=_('Region'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Wine(GenericBaseModel):
    """
    Wine class - inherits from GenericBaseModel
    """

    name = models.CharField(max_length=200, verbose_name=_('Wine Name'))
    description = models.TextField(verbose_name=_('Wine Description'), null=True, blank=True)
    alcohol_percentage = models.FloatField(verbose_name=_('Alcohol(%)'))
    year = models.IntegerField(verbose_name=_('Year'))
    grape_type = models.ManyToManyField(GrapeType, verbose_name=_('Grape Type'), related_name='wines', null=True,
                                        blank=True)
    rating = models.PositiveIntegerField(verbose_name=_('Rating'), default=1,
                                         help_text=_('This field is used wine prices (min=1, max=5)'))
    kind = models.IntegerField(verbose_name=_('Kind'), choices=WINE_KIND_LIST)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Recipe(GenericBaseModel):
    """
    Recipe class - inherits from GenericBaseModel
    """

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    summary = models.CharField(max_length=500, verbose_name=_('Summary'), blank=True, null=True)
    preparation_time = models.CharField(max_length=100, verbose_name=_('Title'), blank=True, null=True)
    difficulty = models.IntegerField(verbose_name=_('Difficulty'), choices=DIFFICULTY_CHOICES)
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    is_for_vegan = models.BooleanField(verbose_name=_('Vegan Friendly'), default=False)
    is_for_vegetarian = models.BooleanField(verbose_name=_('Vegetarian Friendly'), default=False)
    origin = models.ForeignKey(Country, verbose_name=_('Country'))
    image = models.ImageField(verbose_name=_('Image'), upload_to='images', null=True, blank=True)
    suggested_wine = models.ManyToManyField(Wine, verbose_name=_('Suggested Wine'), related_name='recipes', null=True,
                                            blank=True)
    #Use django-tagging application here
    #tags = TagField()
    objects = models.Manager()
    pub_objects = PublishedManager()
    veg_objects = VegManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class RecipeStep(GenericBaseModel):
    """
    RecipeStep class - inherits from GenericBaseModel
    This class represents the step for a recipe preparation
    """
    text = models.TextField(verbose_name=_('Text'), blank=True, null=True)
    recipe = models.ForeignKey(Recipe, verbose_name=_('Recipe'))
    order = models.IntegerField(verbose_name=_('Order'), blank=True, null=True)
    image = models.ImageField(verbose_name=_('Image'), upload_to='images', null=True, blank=True)

    def __unicode__(self):
        ret = self.text[:40]
        if len(self.text) > 40:
            ret += "..."
        return ret

    class Meta:
        ordering = ['order', 'id']


class Unit(models.Model):
    """
    Unit class - inherits from models.Model
    """
    unit_name = models.CharField(max_length=60, verbose_name=_('Unit Name'))
    code = models.CharField(verbose_name=_('Abbreviation Code'), max_length=60, blank=True, null=True)
    type = models.IntegerField(verbose_name=_('Unit Type'), choices=UNIT_TYPE)

    def __unicode__(self):
        return self.unit_name

    class Meta:
        ordering = ['unit_name']


class FoodType(GenericBaseModel):
    """
    FoodType class - inherits from GenericBaseModel
    """
    type_name = models.CharField(max_length=60, verbose_name=_('Ingredient Name'))

    def __unicode__(self):
        return self.type_name

    class Meta:
        ordering = ['type_name']


class Food(GenericBaseModel):
    """
    Food class - inherits from GenericBaseModel
    """
    name = models.CharField(max_length=60, verbose_name=_('Ingredient Name'))
    food_type = models.ForeignKey(FoodType, verbose_name=_('Food type'), related_name='foods')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Ingredient(GenericBaseModel):
    """
    Ingredient class - inherits from GenericBaseModel
    """
    quantity = models.FloatField(verbose_name=_('Unit Type'))
    unit = models.ForeignKey(Unit, verbose_name=_('Unit'), null=True, blank=True)
    recipe = models.ForeignKey(Recipe, verbose_name=_('Recipe'))
    food = models.ForeignKey(Food, verbose_name=_('Food'))
    order = models.PositiveIntegerField(verbose_name=_('Food'), blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Ingredient, self).__init__(*args, **kwargs)

    def __unicode__(self):
        q = str(int(self.quantity) if self.quantity == int(self.quantity) else self.quantity)
        unit = str(self.unit.unit_name if None != self.unit else '')
        food = str(self.food).lower()
        return "%s %s %s" % (q, unit, food)

    class Meta:
        ordering = ['order', 'id']
