from django.shortcuts import render_to_response
from django.template import RequestContext
from repsf.map.models import *
from repsf.map.util import *
from django.core import serializers
import json
from repsf.map.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from repsf.map import util
from django.views.decorators.cache import cache_page

def home(request, location=None, embed=False):
	json_serializer = serializers.get_serializer("json")()
	types 		= Type.objects.filter(parent = None)
	locs		= json_serializer.serialize(Location.objects.all().exclude(lat=None).exclude(type=None), ensure_ascii=True, use_natural_keys = True)
	types_json	= json_serializer.serialize(Type.objects.all(), ensure_ascii=True, use_natural_keys = True)
	try:
		focus = location
	except:
		focus = None 
	
	return render_to_response('map.html', {"types" : types, "locs_json" : locs, "types_json" : types_json, "focus" : focus, "embed" : embed }, context_instance=RequestContext(request) )

@login_required	
def create(request):
	if request.method == "GET":
		form = LocationForm()
		return render_to_response('location_create_form.html', {"form" : form}, context_instance=RequestContext(request))
	elif request.method == "POST":
		newloc = LocationForm(request.POST)
		if newloc.is_valid():
			loc.created_by = request.user
			loc = newloc.save(commit=False)
			geo = util.geocode(loc.address)
			
			if not geo == False:
				loc.lat, loc.lng, loc.fix_address = geo
			else:
				messages.error(request, 'The geocoder says your address is invalid! Can you be more specific?')
				return render_to_response('location_create_form.html', {"form" : newloc, "id":id},context_instance=RequestContext(request))
				
			if newloc.save():
				newloc.save_m2m()
				messages.success(request, 'Location created successfully! We\'ll review it and add it to the map ASAP.')
				return render_to_response('location_create_form.html', {"form" : newloc, "id":id},context_instance=RequestContext(request))
			else:
				messages.error(request, 'Something went wrong, try again')
				return render_to_response('location_create_form.html', {"form" : newloc, "id":id},context_instance=RequestContext(request))
		else:
			messages.error(request, 'Your submission had errors, fix\'er up and try again')
			return render_to_response('location_create_form.html', {"form" : loc, "id":id},context_instance=RequestContext(request))


@login_required	
def update(request, id=None):
	loc = Location.objects.get(pk=id)
	if request.method == "GET":
		form = LocationForm(instance=loc)
		return render_to_response('location_edit_form.html', {"form" : form, "id":id},context_instance=RequestContext(request))
	if request.method == "POST":
		newloc = LocationForm(request.POST, instance=loc)
		if newloc.is_valid():
			if newloc.save():
				messages.success(request, 'Edit successful! We\'ll review it and add it to the map ASAP.')
				return render_to_response('location_edit_form.html', {"form" : newloc, "id":id},context_instance=RequestContext(request))
			else:
				messages.error(request, 'Something went wrong, try again')
				return render_to_response('location_edit_form.html', {"form" : newloc, "id":id},context_instance=RequestContext(request))
		else:
			return render_to_response('location_edit_form.html', {"form" : loc, "id":id},context_instance=RequestContext(request))
		
@login_required	
def _update(request, id=None):
	return render_to_response('sorry.html', {"id":id},context_instance=RequestContext(request))
		
	