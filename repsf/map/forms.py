from django.forms import ModelForm, Select
from repsf.map.models import *

class LocationForm(ModelForm):
	
	class Meta:
		model = Location
		fields = ('name','address','desc','type','hiring')
	