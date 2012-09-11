from django.contrib import admin
from repsf.map.models import *
from django.http import HttpResponse, HttpResponseForbidden
from actions import export_as_csv_action

class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'address','get_types_for_admin','fix_address']
	actions = [export_as_csv_action("CSV Export", fields=['name','address','get_types_for_admin','fix_address'])]
	
admin.site.register(Location, LocationAdmin)

class TypeAdmin(admin.ModelAdmin):
	list_display = ['name', 'label']

admin.site.register(Type, TypeAdmin)

admin.site.register(PendingLocation)