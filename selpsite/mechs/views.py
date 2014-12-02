from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from mechs.models import StdMech

def index(generic.ListView):
  template_name = 'mechs.index/html'
  context_object_name = 'first_mech_list'

  def get_queryset(self):
    """Return the first five mechs."""
    return StdMech.objects.order_by('name')[:5]

def detail(generic.DetailView):
    model = StdMech
    template_name = 'mechs/detail.html'
    # TODO: create detail.html