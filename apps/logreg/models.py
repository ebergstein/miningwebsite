from __future__ import unicode_literals

from django.db import models
import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
IP_REGEX = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

class RegistrationManager(models.Manager):

    def regvalidator(self, email, address, ip, password, confirm):
        errors = []
        if len(email) < 1:
            errors.append("Your email cannot be blank.")
        elif not EMAIL_REGEX.match(email):
            errors.append("Your email must be a valid email.")
        elif User.objects.filter(email = email).exists():
			errors.append("This email is already in use.")
        if len(password) < 8:
            errors.append("Your password must be at least 8 characters long.")
        if password != confirm:
            errors.append("Your confirmation password must match your password.")
        if not IP_REGEX.match(ip):
        	errors.append("Improper IP address.")
        if len(address) < 1:
        	errors.append("Enter Your Address.")
        return {'errors': errors}
        
    def bcryptor(self, password):
        hashword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return {'pwhash': hashword}
        
    def logvalidator(self, email, password):
        errors = []
        # test = User.objects.filter(email = email )
        # print test['email']

        print email
        print password
        try:
            user = User.objects.get(email = email)
            print user

            if bcrypt.hashpw(password.encode('utf8'), user.pwhash.encode('utf8')) == user.pwhash.encode('utf8'):
                return {'user': user, 'errors': errors}
            errors.append("Incorrect password.")
        except:
            errors.append("Unrecognized email address.")
        return {'errors': errors}
        
    def passvalidator(self, id, password, new, confirm):
    	errors = []
    	if new != confirm:
    		errors.append("Confirmation does not match new password.")
    	if len(new) < 8:
            errors.append("Your password must be at least 8 characters long.")
    	try:
            user = User.objects.get(id = id)
            print user

            if bcrypt.hashpw(password.encode('utf8'), user.pwhash.encode('utf8')) != user.pwhash.encode('utf8'):
            	errors.append("Incorrect old password.")
        except:
        	errors.append("User not found.")
        return {'errors': errors}
        
class User(models.Model):
    email = models.EmailField()
    address = models.CharField(max_length = 255)
    ip = models.CharField(max_length = 255)
    pwhash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RegistrationManager()
