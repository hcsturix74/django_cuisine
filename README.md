django_cuisine
=================

Store your recipes with your favourite wines


``django_cuisine`` is a simple django application for managing
your recipes linked to your suggested wines

As I'm fond of cooking, I coded this application to store my favourites recipes
This project is based on django-recipes application which can be found at:
http://code.google.com/p/django-recipes/


Dependecies
-----------
Now it is a stand-alone application.
The only dependency I will introduce is django_tagging



Examples
--------

This is a complete project based on sqlite database

::
python manage.py runserver


ADMIN LOGIN:
  username: admin
  password: admin

You can, of course, delete the DB (djcuisinedb) and perform a syncdb:

python manage.py syncdb

Some fixtures will be inserted soon.
See below and stay tuned!


Application Structure
-----------------------------------------

Wait for a while....Work in progress still!



TODO
-----------------------------------------
- Application Structure ;-)
- Simple front-end and default view(s)
- comments support
- fixtures (with some recipes & wines) -   :-P
- django_tagging
