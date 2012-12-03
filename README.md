django_cuisine
=================

Store your recipes with your favourite wines


``django_cuisine`` is a simple django application for managing
your recipes linked to your suggested wines

As I'm fond of cooking, I coded this application to store my favourites recipes
This project is based on django-recipes application which can be found at:
http://code.google.com/p/django-recipes/

THIS IS A WORK-IN-PROGRESS PROJECT, SO THIS SI NOT A STABLE VERSION.

Dependecies
-----------
Take a look at requirements.txt:
* Django==1.4.2
* Pillow==1.7.8
* django-geo==0.3b1
* django-mptt==0.5.2
* django-social-auth==0.7.10
* django-tagging>=0.3
* httplib2==0.7.7
* oauth2==1.5.211
* python-openid==2.2.5
* wsgiref==0.1.2



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
