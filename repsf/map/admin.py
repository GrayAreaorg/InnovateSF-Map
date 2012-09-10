from django.contrib import admin
from repsf.map.models import Location
from django.http import HttpResponse, HttpResponseForbidden
from actions import export_as_csv_action

class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'address','get_types_for_admin','fix_address']
	actions = [export_as_csv_action("CSV Export", fields=['name','address','get_types_for_admin','fix_address'])]
	
admin.site.register(Location, LocationAdmin)

admin.site.register(Type)