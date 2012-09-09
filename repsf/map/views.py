from django.shortcuts import render_to_response
from django.template import RequestContext
from repsf.map.models import *
from repsf.map.util import *
from django.core import serializers
import json

def home(request):
	json_serializer = serializers.get_serializer("json")()
	types 		= Type.objects.filter(parent = None)
	locs		= json_serializer.serialize(Location.objects.all(), ensure_ascii=True, use_natural_keys = True)
	types_json	= json_serializer.serialize(Type.objects.all(), ensure_ascii=True, use_natural_keys = True)
	
	return render_to_response('map.html', {"types" : types, "locs_json" : locs, "types_json" : types_json }, context_instance=RequestContext(request) )