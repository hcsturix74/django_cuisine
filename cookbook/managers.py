__author__ = 'Luca'

from django.db import models
from django.db.models import Q


class PublishedManager(models.Manager):
    """
    This manager implements the get_query_set() method
    and  filters only the published 'contents'
    """

    def get_query_set(self):
        """
        This is the get_query_set method override.
        Here only published stuff is retrieved; this filter is on
        is_published field.
        """
        return super(PublishedManager, self).get_query_set().filter(is_published=True)


class VegManager(models.Manager):
    """
    This manager implements the get_query_set() method
    and  filters only the published 'contents'
    """

    def get_query_set(self):
        """
        This is the get_query_set method override.
        Here only published stuff is retrieved; this filter is on
        is_published field.
        """
        return super(VegManager, self).get_query_set().filter(
            Q(is_published=True) & (Q(is_for_vegan=True) | Q(is_for_vegetarian=True)))

    def vegan_friendly(self):
        """
        This method filters vegan_friendly recipes.
        Here only published stuff and vegan recipes are retrieved;
        """
        return super(VegManager, self).get_query_set().filter(is_published=True, is_for_vegan=True)

    def vegetarian_friendly(self):
        """
        This method filters vegetarian_friendly recipes.
        Here only published stuff and vegetarian recipes are retrieved;
        """
        return super(VegManager, self).get_query_set().filter(is_published=True, is_for_vegetarian=True)

