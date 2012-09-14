from django.forms import ModelForm, Select
from repsf.map.models import *

class LocationForm(ModelForm):
	"""def current_user_is_owner(self):
		if not self.instance:
			return False
		
		if not self.request:
			return False
		
		if not self.request.get('user', False):
			return False
		
		if self.request.get('user') == instance.get('owner', False):
			return True
		else:
			return False"""
	
	class Meta:
		model = Location
		fields = ('name','address','desc')
	