from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User

def index(request):
    return render(request, 'logreg/index.html')

def register(request):
    user = User.objects.regvalidator(request.POST['email'], request.POST['password'], request.POST['confirm'], 
    request.POST['address'], request.POST['ip'])
    if user['errors'] != []:
        for errors in user['errors']:
            messages.add_message(request, messages.ERROR, errors)
        return redirect(reverse('login:home'))
    prehash = User.objects.bcryptor(request.POST['password'])
    pwhash = prehash['pwhash']
    User.objects.create(email = request.POST['email'], pwhash = pwhash, 
    address = request.POST['address'], ip = request.POST['ip'])
    request.session['email'] = request.POST['email']
    check = User.objects.get(email = request.POST['email'])
    request.session['id'] = check.id
    request.session['address'] = check.address 
    return redirect(reverse('mining:home'))

def login(request):
    user = User.objects.logvalidator(request.POST['email'], request.POST['password'])
    if user['errors'] != []:
        for errors in user['errors']:
            messages.add_message(request, messages.ERROR, errors)
        return redirect(reverse('login:home'))
    namer = User.objects.get(email = request.POST['email'])
    request.session['id'] = namer.id
    request.session['address'] = namer.address
    return redirect(reverse('mining:home'))