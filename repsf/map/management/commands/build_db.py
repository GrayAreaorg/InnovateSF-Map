from django.core.management.base import BaseCommand, CommandError
from repsf.map.models import *
from optparse import make_option
from geopy import geocoders
import requests
import json
import math
import time

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    option_list = BaseCommand.option_list + (
        make_option('--city',
            dest='city',
            help='Enter the name of a city'),
         make_option('--range',
                dest='range',
                help='Enter a numerical range to search'),
        )
    
    def loop(self, city, range, page):
        r = requests.get("http://api.crunchbase.com/v/1/search.js?geo=%s&range=%s&page=%s" % (city, range, page))
        return json.loads(r.content)
        
    
    def handle(self, *args, **options):
        g = geocoders.Google()
        r = requests.get("http://api.crunchbase.com/v/1/search.js?geo=%s&range=%s" % (options['city'], options['range']))
        cache = {}
        
        if r.status_code != 200:
            print "Couldn't find anything, server returned error %s. Message:'%s'" % (r.status_code, r.content)
            
        print 'Got results'
        j = json.loads(r.content)
        pages = int( math.ceil( float(j['total']) / float( len(j['results']) ) ) ) - 1
        page = 0
        print 'There are %s pages of data' % pages
        
        while page <= pages:
            page = page + 1
            r = self.loop(options['city'], options['range'], page)['results']
            print 'Doing page %s of %s' % (page, pages)
            for result in r:
                fix_address = False
				
                if not result['offices']:
                    continue
                
                try:
                    result['offices'] = [o for o in result['offices'] if options['city'] in o['city']]
                except:
                    print "something went wrong here"
                    continue
                
                if not result.get('offices', False): #Is there an SF office?
                    print "Found no %s office for %s \n" % (options['city'], result['name'])
                    continue
                
                print 'Doing %s' % result['name']
                
                #OK, we got this far. Before we do any address lookup, we need to check if the company was deadpooled.
                company = json.loads(requests.get("http://api.crunchbase.com/v/1/%s/%s.json" % (result['namespace'], result['permalink'])).content)
                
                if company.get('deadpooled_year', False):
                    print 'DEADPOOLED!'
                    continue
                
                #are they already in the DB? (for data-gathering error recovery)
                
                l, created_l = Location.objects.get_or_create(name = result['name'])
				
                if not created_l:
                    continue
                
                office = result['offices'][0]

                search_address = "%s %s %s %s %s" % (office.get('address1',''), office.get('address2',''), office.get('city',''), office.get('state_code',''), office.get('zip_code','') )
                search_address = search_address.replace('None','')
                
                if not cache.get(search_address, False):
                    try:
                        geo = g.geocode(search_address, exactly_one = False)
                        if len(geo) > 1:
                            print "We're using the first location found, but mark it for fixing so it gets checked"
                            fix_address = True

                        place, (lat, lon) = geo[0]
                        cache[search_address] = (lat, lon)
                    except:
                        print "couldn't find location."
                        if not cache.get(options['city'], False):
                            geo = g.geocode(options['city'], exactly_one = False)
                            place, (lat, lon) = geo[0]
                        else:
                            (lat, lon) = cache[options['city']]
                else:
                    (lat, lon) = cache[search_address]
                
                if not office['address1']:
                    fix_address = True
                
                types = []
                obj, created = Type.objects.get_or_create(name = result['namespace'])
                types.append(obj)
                
                if company.get('category_code', False):
                	obj, created = Type.objects.get_or_create(name = company['category_code'], parent = types[0])
                	types.append(obj)
				
                l.lat = lat
                l.lng = lon
                l.address = search_address
                l.name = result['name']
                l.permalink = result['permalink']
                l.desc = result['overview']
                l.fix_address = fix_address
                l.save()
                for type in types:
                    l.type.add(type)
                time.sleep(1)
        print "\a \a \a winner winner chicken dinner"
                    
            
            
        