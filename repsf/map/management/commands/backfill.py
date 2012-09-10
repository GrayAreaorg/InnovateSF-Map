from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from repsf.map.models import *
from optparse import make_option
from geopy import geocoders
import requests
import json
import math
import time

class Command(NoArgsCommand):
	def handle_noargs(self):
		l = Location.objects.all()
		for location in l:
			namespace = location.type.filter(parent=None)[0]
			try:
				r = requests.get("http://api.crunchbase.com/v/1/%s/%s.js" % (namespace, l.name))
				j = json.loads(r)
			except:
				print "Something went wrong, logo couldn't be loaded! \n"