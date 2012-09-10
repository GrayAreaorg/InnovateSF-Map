# Create your views here.
from emailusernames.utils import create_user
from django.shortcuts import render_to_response
from django.template import RequestContext
from emailusernames.forms import EmailUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def create(request):
	if request.method == 'GET':
		form = EmailUserCreationForm()
		return render_to_response('create.html', {'form':form}, context_instance=RequestContext(request))
	if request.method == 'POST':
		form = EmailUserCreationForm(request.POST)
		if form.is_valid():
			user = create_user(request.POST['email'], request.POST['password1'])
			user.save()
			return render_to_response('thanks.html', {'user':user}, context_instance=RequestContext(request))
		else:
			return render_to_response('create.html', {'form':form}, context_instance=RequestContext(request))

@login_required
def read(request):
	if request.user.is_authenticated():
		return render_to_response('profile.html', {'user':request.user}, context_instance=RequestContext(request))

@login_required
def end_session(request):
	logout(request)
	return render_to_response('thanks.html', context_instance=RequestContext(request))