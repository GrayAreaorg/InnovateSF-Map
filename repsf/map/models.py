from django.db import models
from geopy import geocoders
from django.contrib.auth.models import User

class Location(models.Model):
	lat 		= models.DecimalField(max_digits=15, decimal_places=10, blank = True, null = True)
	lng 		= models.DecimalField(max_digits=15, decimal_places=10, blank = True, null = True)
	address		= models.TextField()
	name		= models.CharField(max_length = 256, unique=True)
	permalink	= models.CharField(max_length = 256, blank=True, null=True)
	desc		= models.TextField(blank = True, null=True, verbose_name='Description')
	type		= models.ManyToManyField("Type")
	hiring      = models.BooleanField(verbose_name='Are you hiring?')
	fix_address = models.BooleanField()
	owner		= models.ForeignKey(User, null = True, related_name='owner')
	created_by	= models.ForeignKey(User, null = True, related_name='creator')
	__original_name = None
	
	def __unicode__(self):
		return self.name

	def get_types_for_admin(self):
		return "\n".join([t.name for t in self.type.all()])
	
	get_types_for_admin.admin_order_field = 'type'
	
	def __init__(self, *args, **kwargs):
		super(Location, self).__init__(*args, **kwargs)
		self.__original_address = self.address
	
	def save(self, force_insert=False, force_update=False):
		if self.address != self.__original_address or not self.lat:
			g = geocoders.Google()
			geo = False
			try:
				geo = g.geocode(self.address, exactly_one = False)
				if len(geo) > 1:
					self.fix_address = True                	
			except:
				#REFACTOR FOR ANY CITY
				geo = g.geocode('San Francisco', exactly_one = False)
				self.fix_address = True
				
			if geo:
				place, (self.lat, self.lng) = geo[0]
		
		if self.type.all() == []:
			self.type.add(m.Type.objects.get(name="company"))

		super(Location, self).save(force_insert, force_update)
		self.__original_address = self.address
	
	class Meta:
		ordering = ['name']

class Type(models.Model):
	name		= models.CharField(max_length=256, null = True, blank = True)
	label		= models.CharField(max_length=256, null=True, blank=True)
	parent 		= models.ForeignKey('self', null=True, blank=True)
	
	def __unicode__(self):
		return self.name
	
	def natural_key(self):
		try:
			id = self.parent.id
		except:
			id = 0
		return { self.name:id }
	
	class Meta:
		ordering = ['name']
	