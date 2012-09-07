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
	cache = {}

	while page <= pages:
		page += 1
		fix_address = False
		print 'Getting page %s of %s' % (page, pages)
		results = loop(city, range, page)['results']
		for result in results:
			#Filter out non-SF offices, the Crunchbase API returns false positives.
			result['offices'] = [v for k,v in enumerate(result['offices']) if city in v['city']]
			if result['offices']: #Is there an SF office?
				print "Found %s office for %s" % (city, result['name'])
				print result['offices'][0]
                #office = result['offices'][0]
                office = "blah"
                #search_address = "%s %s %s %s %s" % (office.get('address1',''), office.get('address2',''), office.get('city',''), office.get('state_code',''), office.get('zip_code','') )
                search_address = "San Francisco"
                print search_address
                search_address = search_address.replace('None ','')
                print search_address
                print "uh, bro?"
                print "searching for %s" % search_address
                #And Google that shit
                if not cache.get(search_address, False):
                    geo = g.geocode(search_address, exactly_one = False)
                    if len(geo) > 1:
                        print "We're using the first location found, but mark it for fixing so it gets checked"
                        fix_address = True

                    place, (lat, lon) = geo[0]
                    print 'Found better coordinates'
                    cache[search_address] = (lat, lon)
                else:
                    (lat, lon) = cache[search_address]
                
                if not office['address1']:
                    fix_address = True
				
                types = []
                obj, created = Type.objects.get_or_create(name = result['namespace'])
                types.append(obj)
                j = json.loads(requests.get("http://api.crunchbase.com/v/1/%s/%s.json" % (result['namespace'], result['permalink'])).content)
                if 'category_code' in j:
                	if j['category_code'] != None:
                		obj, created = Type.objects.get_or_create(name = j['category_code'], parent = types[0])
                		types.append(obj)
				
                l = Location(
					lat 		= lat,
	                lng 		= lon,
	               	address		= search_address,
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
		