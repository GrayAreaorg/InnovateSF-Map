from django.shortcuts import render_to_response
from django.template import RequestContext
from repsf.map.models import *
from repsf.map.util import *
from django.core import serializers
import json
from repsf.map.forms import *

def home(request, location=None):
	json_serializer = serializers.get_serializer("json")()
	types 		= Type.objects.filter(parent = None)
	locs		= json_serializer.serialize(Location.objects.all(), ensure_ascii=True, use_natural_keys = True)
	types_json	= json_serializer.serialize(Type.objects.all(), ensure_ascii=True, use_natural_keys = True)
	try:
		focus = location
	except:
		focus = None 
	
	return render_to_response('map.html', {"types" : types, "locs_json" : locs, "types_json" : types_json, "focus" : focus }, context_instance=RequestContext(request) )
	
def update(request):
	if request.GET:
		form = LocationForm()
		return render_to_response('form.html', {"form" : form})