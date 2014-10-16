from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

from mechs.models import StdMech

def index(request):
  first_mech_list = StdMech.objects.order_by('name')[:5]
  #template = loader.get_template('mechs/index.html')
  context = {'first_mech_list': first_mech_list}
  return render(request, 'mechs/index.html', context)

def detail(request, mech_id):
  return HttpResponse("You're looking at mech %s." % mech_id)