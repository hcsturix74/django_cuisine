from django.conf.urls.defaults import patterns, url

from django.views.generic import (ListView,
                                 CreateView,
                                 UpdateView,
                                 DeleteView
                                 )

from cookbook.forms import RecipeForm, WineForm

def cookbook_patterns(*forms, **kwargs):
    patterns_ = patterns('')
    for form in forms:
        patterns_ += cookbook_pattern(form, **kwargs)
    return patterns_

def cookbook_pattern(form, **kwargs):
    model = form._meta.model
    name = model._meta.object_name.lower()

    urls = []

    if 'list_view' not in kwargs or kwargs.get('list_view') is not None:
        view = kwargs.get('list_view', ListView).as_view(model=model)
        url_ = kwargs.get('list_view_url', r'^%s/$' % name)
        urls.append(cookbook_list(url_, view=view, name='%s_list' % name))

    if 'create_view' not in kwargs or kwargs.get('create_view') is not None:
        view = kwargs.get('create_view', CreateView).as_view(form_class=form,model=model)
        url_ = kwargs.get('create_view_url', r'^%s/add/$' % name)
        urls.append(cookbook_create(url_, view=view, name='%s_form' % name))

    if 'update_view' not in kwargs or kwargs.get('update_view') is not None:
        view = kwargs.get('update_view', UpdateView).as_view(form_class=form,model=model)
        url_ = kwargs.get('update_view_url', r'^%s/(?P<pk>\d+)/$' % name)
        urls.append(cookbook_update(url_, view=view, name='%s_form' % name))

    if 'delete_view' not in kwargs or kwargs.get('delete_view') is not None:
        view = kwargs.get('delete_view', DeleteView).as_view(model=model)
        url_ = kwargs.get('delete_view_url', r'^%s/(?P<pk>\d+)/delete/$' % name)
        urls.append(cookbook_delete(url_, view=view, name='%s_delete' % name))

    return patterns('', *urls)

def cookbook_list(url_, name, view=None, model=None):
    #print view
    if view is None:
        view = ListView.as_view(model=model)
    return url(url_, view, name=name)


def cookbook_create(url_, name, view=None, form=None):
    if view is None:
        view = CreateView.as_view(form_class=form)
    return url(url_, view, name=name)


def cookbook_update(url_, name, view=None, form=None):
    if view is None:
        view = UpdateView.as_view(form_class=form)
    return url(url_, view, name=name)


def cookbook_delete(url_, name, view=None, model=None):
    if view is None:
        view = DeleteView.as_view(model=model)
    return url(url_, view, name=name)

urlpatterns = cookbook_patterns(RecipeForm)
urlpatterns += cookbook_patterns(WineForm)
