from django.db import models

class Location(models.Model):
	lat 		= models.DecimalField(max_digits=15, decimal_places=10, blank = True, null = True)
	lng 		= models.DecimalField(max_digits=15, decimal_places=10, blank = True, null = True)
	address		= models.TextField(blank=True, null=True)
	name		= models.CharField(max_length = 256, unique=True)
	permalink	= models.URLField()
	desc		= models.TextField(blank = True, null=True)
	type		= models.ManyToManyField("Type")
	fix_address = models.BooleanField()
	def __unicode__(self):
		return self.name
	
	def get_types_for_admin(self):
	  return "\n".join([t.name for t in self.type.all()])

class Type(models.Model):
	name		= models.CharField(max_length=256, null = True, blank = True)
	parent 		= models.ForeignKey('self', null=True, blank=True)
	
	def __unicode__(self):
		return self.name
	
	def natural_key(self):
		try:
			id = self.parent.id
		except:
			id = 0
		return { self.name:id }
	