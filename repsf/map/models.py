from django.db import models
from geopy import geocoders

class Location(models.Model):
	lat 		= models.DecimalField(max_digits=15, decimal_places=10, blank = True, null = True)
	lng 		= models.DecimalField(max_digits=15, decimal_places=10, blank = True, null = True)
	address		= models.TextField(blank=True, null=True)
	name		= models.CharField(max_length = 256, unique=True)
	permalink	= models.CharField(max_length = 256, blank=True, null=True)
	desc		= models.TextField(blank = True, null=True)
	type		= models.ManyToManyField("Type")
	hiring      = models.BooleanField()
	fix_address = models.BooleanField()
	__original_name = None
	
	def __unicode__(self):
		return self.name

	def get_types_for_admin(self):
		return "\n".join([t.name for t in self.type.all()])
	
	def __init__(self, *args, **kwargs):
		super(Location, self).__init__(*args, **kwargs)
		self.__original_address = self.address
	
	def save(self, force_insert=False, force_update=False):
		if self.address != self.__original_address:
			g = geocoders.Google();
			try:
				geo = g.geocode(search_address, exactly_one = False)
				if len(geo) > 1:
					self.fix_address = True                
				place, (lat, lon) = geo[0]
			except:
				pass
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
	