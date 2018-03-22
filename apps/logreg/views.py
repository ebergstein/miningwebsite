from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User

def index(request):
    return render(request, 'logreg/index.html')

def register(request):
    user = User.objects.regvalidator(request.POST['username'], request.POST['email'], request.POST['password'], request.POST['confirm'])
    if user['errors'] != []:
        for errors in user['errors']:
            messages.add_message(request, messages.ERROR, errors)
        return redirect(reverse('login:home'))
    prehash = User.objects.bcryptor(request.POST['password'])
    pwhash = prehash['pwhash']
    User.objects.create(username = request.POST['username'], email = request.POST['email'], pwhash = pwhash)
    request.session['username'] = request.POST['username']
    check = User.objects.get(email = request.POST['email'])
    request.session['id'] = check.id
    request.session['username'] = check.username 
    return redirect(reverse('mining:home'))

def login(request):
    user = User.objects.logvalidator(request.POST['email'], request.POST['password'])
    if user['errors'] != []:
        for errors in user['errors']:
            messages.add_message(request, messages.ERROR, errors)
        return redirect(reverse('login:home'))
    namer = User.objects.get(email = request.POST['email'])
    request.session['id'] = namer.id
    request.session['username'] = namer.username
    return redirect(reverse('mining:home'))