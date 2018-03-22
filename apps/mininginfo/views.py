from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from ..logreg.models import User

# Create your views here.

def index(request):
	try:
		user = User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	return render(request, 'mininginfo/index.html')
    
def logout(request):
	try:
		User.objects.get(id = request.session['id'])
	except:
		return redirect(reverse('login:home'))
	del request.session['username']
	return redirect(reverse('login:home'))