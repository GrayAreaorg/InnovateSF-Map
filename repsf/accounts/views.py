# Create your views here.
from emailusernames.utils import create_user
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from emailusernames.forms import EmailUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages


def create(request):
	if request.method == 'GET':
		form = EmailUserCreationForm()
		return render_to_response('create.html', {'form':form}, context_instance=RequestContext(request))
	if request.method == 'POST':
		form = EmailUserCreationForm(request.POST)
		if form.is_valid():
			user = create_user(request.POST['email'], request.POST['password1'])
			user.save()
			messages.success(request,'New user successfully created! Go ahead and log in.')
			return redirect('/accounts/login')
		else:
			return render_to_response('create.html', {'form':form}, context_instance=RequestContext(request))

@login_required
def read(request):
	if request.user.is_authenticated():
		return render_to_response('profile.html', {'user':request.user}, context_instance=RequestContext(request))

@login_required
def end_session(request):
	logout(request)
	return redirect('/')