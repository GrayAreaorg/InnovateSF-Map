from django.contrib import admin
from repsf.map.models import Location

class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'address', 'fix_address']
	
admin.site.register(Location, LocationAdmin)