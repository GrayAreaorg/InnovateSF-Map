from django.forms import ModelForm
from repsf.map.models import *

class LocationForm(ModelForm):
	class Meta:
		model = Location
		exclude = ('lat','lng','fix_address')
	