from emailusernames.forms import EmailAuthenticationForm

class ISFAuthForm(EmailAuthenticationForm):
	def __init__(self, *args, **kw):
		super(EmailAuthenticationForm, self).__init__(*args, **kw)
		self.fields.keyOrder = [
	            'email',
				'password'
			]