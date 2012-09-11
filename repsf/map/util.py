from models import *
from geopy import geocoders
import json
import requests
import math

def loop(city, range, page):
	r = requests.get("http://api.crunchbase.com/v/1/search.js?geo=%s&range=%d&page=%d" % (city, range, page))
	return json.loads(r.content)

def geocode(address):
	g = geocoders.Google()
	fix_address = False
	try:
		geo = g.geocode(address, exactly_one=False)
	except:
		return False
	
	if len(geo) > 1:
		fix_address = True
		
	place, (lat, lng) = geo[0]
	
	return (lat, lng, fix_address)
				
def types_to_dict(toptypes):
	the_json = []
	for t in toptypes:
		json_chunk = {
			'name': t.name,
			'subtypes': [subtype.name for subtype in t.type_set.all()]
		}
		the_json.append(json_chunk)
	return the_json
		