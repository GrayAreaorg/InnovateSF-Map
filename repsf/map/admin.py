from django.contrib import admin
from repsf.map.models import Location

admin.site.register(Location)

class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'address', 'fix_address']