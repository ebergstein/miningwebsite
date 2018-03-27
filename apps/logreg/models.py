from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class RegistrationManager(models.Manager):

	def regvalidator(self, email, password, confirm):
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
		return {'errors': errors}
	def bcryptor(self, password):
		hashword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		return {'pwhash': hashword}
	def logvalidator(self, email, password):
		errors = []
		try:
			user = User.objects.get(email = email)
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
			if bcrypt.hashpw(password.encode('utf8'), user.pwhash.encode('utf8')) != user.pwhash.encode('utf8'):
				errors.append("Incorrect old password.")
		except:
			errors.append("User not found.")
		return {'errors': errors}
    	
class User(models.Model):
	email = models.EmailField()
	pwhash = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = RegistrationManager()