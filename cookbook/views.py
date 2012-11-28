# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext



def homepage(request):
    """
    Just a simple homepage
    """
    return render_to_response("homepage.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request))