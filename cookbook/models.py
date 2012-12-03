# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
import datetime
from filer.fields import image

from geo.models import AdministrativeArea, Country, Location
from tagging.fields import TagField
from managers import VegManager, PublishedManager

#Some choices here
DIFFICULTY_CHOICES = ((1, _(u'Very Easy')),
                      (2, _(u'Easy')),
                      (3, _(u'Medium')),
                      (4, _(u'Difficult')),
                      (5, _(u'Very Difficult')),)

#unit type, for Weight, Volume or other....
UNIT_TYPE = ((1, _(u'Weight')),
             (2, _(u'Volume')),
             (3, _(u'Other')),)

WINE_KIND_LIST = ((1, _(u'Red')),
                 (2, _(u'White')),
                 (3, _(u'Rosè')),
                 (4, _(u'Sparkling')),
                 (5, _(u'Passito')),
                 (6, _(u'Liqueur-like')),)

DOP = 1
IGP = 2
EU_OTHER = 3
WINE_EUROPEAN_TYPES = ((DOP, _(u'DOP')),
                      (IGP, _(u'IGP')),
                      (EU_OTHER, _(u'Other')),)

DOCG = 1
DOC = 2
IGT = 3
TR_OTHER = 4
WINE_TRADITIONAL_TYPES = ((DOCG, _(u'DOCG')),
                         (DOC, _(u'DOC')),
                         (IGT, _(u'IGT')),
                         (TR_OTHER, _(u'Other')),)

class GenericBaseModel(models.Model):
    """
    GenericBaseModel class - inherits from models.Model
    This class is an abstract structure for site
    content (not translatable fields, see GenericBaseTranslationModel) management
    It provides some basic attributes (i.e. table columns) common to Content base
    applications
    """
    is_published = models.BooleanField(blank=True, default=True, verbose_name=_(u'Published'))
    created = models.DateTimeField(verbose_name=_(u'Creation Date'), default=datetime.datetime.now(), editable=False)
    updated = models.DateTimeField(verbose_name=_(u'Modify Date'), default=datetime.datetime.now(), editable=False)
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
    name = models.CharField(verbose_name=_(u'Category'), max_length=60, blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name=_(u'Parent'))
    order = models.IntegerField(verbose_name=_(u'Order'), blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')


class GrapeType(GenericBaseModel):
    """
    GrapeType class - inherits from GenericBaseModel
    """

    name = models.CharField(max_length=200, verbose_name=_(u'Grape Name'))
    origin = models.CharField(max_length=200, verbose_name=_(u'Origin'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Wine(GenericBaseModel):
    """
    Wine class - inherits from GenericBaseModel
    """

    name = models.CharField(max_length=200, verbose_name=_(u'Wine Name'))
    description = models.TextField(verbose_name=_(u'Wine Description'), null=True, blank=True)
    image = image.FilerImageField(verbose_name=_(u'Image'), null=True, blank=True)
    code = models.CharField(max_length=20, verbose_name=_(u'Code'))
    traditional_code = models.IntegerField(verbose_name=_(u'Traditional Code'), choices=WINE_TRADITIONAL_TYPES,
                                           default=1)
    european_code = models.IntegerField(verbose_name=_(u'EU Code'), choices=WINE_EUROPEAN_TYPES, default=1)
    place = models.ForeignKey(Location,verbose_name=_(u'Location'), null=True, blank=True)
    cooperative = models.CharField(max_length=200, verbose_name=_(u'Cooperative'), null=True, blank=True)
    area = models.ForeignKey(AdministrativeArea, verbose_name=_(u'Area'))
    suggest_temperature = models.IntegerField(verbose_name=_(u'Temperature(°C)'), null=True, blank=True)
    estate_bottled = models.BooleanField(verbose_name=_(u'Estate Bottled'), default=False)
    alcohol_percentage = models.FloatField(verbose_name=_(u'Alcohol(%)'))
    year = models.IntegerField(verbose_name=_(u'Year'))
    grape_type = models.ManyToManyField(GrapeType, verbose_name=_(u'Grape Type'), related_name='wines', null=True,
                                        blank=True)
    rating = models.PositiveIntegerField(verbose_name=_(u'Rating'), default=1,
                                         help_text=_(u'This field is used wine prices (min=1, max=5)'))
    kind = models.IntegerField(verbose_name=_(u'Kind'), choices=WINE_KIND_LIST)
    tags = TagField()


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Recipe(GenericBaseModel):
    """
    Recipe class - inherits from GenericBaseModel
    """

    title = models.CharField(max_length=200, verbose_name=_(u'Title'))
    summary = models.CharField(max_length=500, verbose_name=_(u'Summary'), blank=True, null=True)
    preparation_time = models.CharField(max_length=100, verbose_name=_(u'Title'), blank=True, null=True)
    difficulty = models.IntegerField(verbose_name=_(u'Difficulty'), choices=DIFFICULTY_CHOICES)
    category = models.ForeignKey(Category, verbose_name=_(u'Category'))
    is_for_vegan = models.BooleanField(verbose_name=_(u'Vegan Friendly'), default=False)
    is_for_vegetarian = models.BooleanField(verbose_name=_(u'Vegetarian Friendly'), default=False)
    area = models.ForeignKey(AdministrativeArea, verbose_name=_(u'Area'), null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name=_(u'Country'))
    image = image.FilerImageField(related_name="recipes",verbose_name=_(u'Image'), null=True, blank=True)
    suggested_wine = models.ManyToManyField(Wine, verbose_name=_(u'Suggested Wine'), related_name='recipes', null=True,
                                            blank=True)
    author = models.ForeignKey(User, verbose_name=_(u'Author'))
    fork_origin = models.ForeignKey('self', verbose_name=_(u'Fork Origin'), blank=True, null=True)
    #Use django-tagging application here
    tags = TagField()
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
    text = models.TextField(verbose_name=_(u'Text'), blank=True, null=True)
    recipe = models.ForeignKey(Recipe, verbose_name=_(u'Recipe'))
    order = models.IntegerField(verbose_name=_(u'Order'), blank=True, null=True)
    duration = models.IntegerField(verbose_name=_(u'Duration (min.)'), blank=True, null=True)
    image = image.FilerImageField(related_name="recipes_steps",verbose_name=_(u'Image'),null=True, blank=True)

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
    unit_name = models.CharField(max_length=60, verbose_name=_(u'Unit Name'))
    code = models.CharField(verbose_name=_(u'Abbreviation Code'), max_length=60, blank=True, null=True)
    type = models.IntegerField(verbose_name=_(u'Unit Type'), choices=UNIT_TYPE)

    def __unicode__(self):
        return self.unit_name

    class Meta:
        ordering = ['unit_name']


class FoodType(GenericBaseModel):
    """
    FoodType class - inherits from GenericBaseModel
    """
    type_name = models.CharField(max_length=60, verbose_name=_(u'Ingredient Name'))

    def __unicode__(self):
        return self.type_name

    class Meta:
        ordering = ['type_name']


class Food(GenericBaseModel):
    """
    Food class - inherits from GenericBaseModel
    """
    name = models.CharField(max_length=60, verbose_name=_(u'Ingredient Name'))
    food_type = models.ForeignKey(FoodType, verbose_name=_(u'Food Type'), related_name='foods')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Ingredient(GenericBaseModel):
    """
    Ingredient class - inherits from GenericBaseModel
    """
    quantity = models.FloatField(verbose_name=_(u'Quantity'))
    unit = models.ForeignKey(Unit, verbose_name=_(u'Unit'), null=True, blank=True)
    recipe = models.ForeignKey(Recipe, verbose_name=_(u'Recipe'))
    food = models.ForeignKey(Food, verbose_name=_(u'Food'))
    order = models.PositiveIntegerField(verbose_name=_(u'Order'), blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Ingredient, self).__init__(*args, **kwargs)

    def __unicode__(self):
        q = str(int(self.quantity) if self.quantity == int(self.quantity) else self.quantity)
        unit = str(self.unit.unit_name if None != self.unit else '')
        food = str(self.food).lower()
        return "%s %s %s" % (q, unit, food)

    class Meta:
        ordering = ['order', 'id']
