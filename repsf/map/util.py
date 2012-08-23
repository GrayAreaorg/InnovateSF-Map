from models import *
from geopy import geocoders
import json
import requests
import math

g = geocoders.Google()

def loop(city, range, page):
	r = requests.get("http://api.crunchbase.com/v/1/search.js?geo=%s&range=%d&page=%d" % (city, range, page))
	return json.loads(r.content)

def build_db(city, range):
	#run this once for your city!
	r = requests.get("http://api.crunchbase.com/v/1/search.js?geo=%s&range=%d" % (city, range))
	
	if r.status_code != 200:
		print "Couldn't find anything, server returned error %s. Message:'%s'" % (r.status_code, r.content)
		return False
	
	print 'Got results'
	j = json.loads(r.content)

	pages = int( math.ceil( float(j['total']) / float( len(j['results']) ) ) ) - 1
	page = 0

	while page <= pages:
		page += 1
		fix_address = False
		print 'Getting page %s of %s' % (page, pages)
		results = loop(city, range, page)['results']
		for result in results:
			#Filter out non-SF offices, the Crunchbase API returns false positives.
			result['offices'] = [v for k,v in enumerate(result['offices']) if v['city'] == city]
			if result['offices']: #Is there an SF office?
				print "Found %s office for %s" % (city, result['name'])
				#Find types. Only companies have sub-types, but we want to filter on them
				types = []
				obj, created = Type.objects.get_or_create(name = result['namespace'])
				types.append(obj)
				j = json.loads(requests.get("http://api.crunchbase.com/v/1/%s/%s.json" % (result['namespace'], result['permalink'])).content)
				if 'category_code' in j:
					if j['category_code'] != None:
						obj, created = Type.objects.get_or_create(name = j['category_code'], parent = types[0])
						types.append(obj)
					
				#Fix address stupidity. The Crunchbase API returns the same lat lng for 90% of the companies:
				#"latitude": 37.775196, "longitude": -122.419204. THIS IS ONLY FOR SF, REFACTOR THIS
				#Check for this latlng first. We will assume it's wrong and there's better data elsewhere.
				
				if (result['offices'][0]['latitude'] == 37.775196 and result['offices'][0]['longitude'] == -122.419204) or (not result['offices'][0]['latitude'] or not result['offices'][0]['longitude']) :
					#Cruchbase gave us the wrong coordinates! Cool! Is there an address?
					print "Wrong coordinates, finding better ones..."
					if result['offices'][0]['address1']:
						#Cool, now we can get the actual coordinates. Construct an address...
						search_address = "%s %s %s %s %s" % (result['offices'][0]['address1'], result['offices'][0]['address2'], result['offices'][0]['city'], result['offices'][0]['state_code'], result['offices'][0]['zip_code'])
						print "searching for %s" % search_address
						#And Google that shit
						geo = g.geocode(search_address, exactly_one = False)
						if len(geo) > 1:
							print "We're using the first location found, but mark it for fixing so it gets checked"
							fix_address = True
						place, (result['offices'][0]['latitude'], result['offices'][0]['longitude']) = geo[0]
						print 'Found better coordinates'
					else:
						print 'No address! Fixme!'
						fix_address = True
						
					#If there's no address, there's nothing we can do except cluster the location markers.
				
				l = Location(
					lat 		= result['offices'][0]['latitude'],
	                lng 		= result['offices'][0]['longitude'],
	               	address		= "%s %s %s %s" % (result['offices'][0]['address1'], result['offices'][0]['address2'], result['offices'][0]['city'], result['offices'][0]['state_code']),
	               	name		= result['name'],
	               	permalink	= result['permalink'],
	               	desc		= result['overview'],
					fix_address = fix_address
				)
				l.save()
				for type in types:
					l.type.add(type)
	print "\a \a \a winner winner chicken dinner"
				
def types_to_dict(toptypes):
	the_json = []
	for t in toptypes:
		json_chunk = {
			'name': t.name,
			'subtypes': [subtype.name for subtype in t.type_set.all()]
		}
		the_json.append(json_chunk)
	return the_json
		