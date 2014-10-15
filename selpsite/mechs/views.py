from django.shortcuts import render
from django.http import HttpResponse
from mechs.models import StdMech

def index(request):
    first_mech_list = StdMech.objects.order_by('name')[:5]
    output = "<b>Some mechs:</b><br>" + ',<br>'.join([p.name for p in first_mech_list])
    return HttpResponse(output)

def detail(request, mech_id):
    return HttpResponse("You're looking at mech %s." % mech_id)