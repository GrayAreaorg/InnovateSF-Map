# Create your views here.
from emailusernames.utils import create_user
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from emailusernames.forms import EmailUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
import json


def create(request):
	if request.method == 'GET':
		form = EmailUserCreationForm()
		return render_to_response('create.html', {'form':form}, context_instance=RequestContext(request))
	if request.method == 'POST':
		form = EmailUserCreationForm(request.POST)
		if form.is_valid():
			user = create_user(request.POST['email'], request.POST['password1'])
			user.save()
			messages.success(request,'New user successfully created! Go ahead and log in right here.')
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

def is_logged_in(request):
	status = {'logged_in':request.user.is_authenticated()}
	return HttpResponse(json.dumps(status),'application/json')