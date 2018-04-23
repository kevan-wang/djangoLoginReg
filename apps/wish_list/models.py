from __future__ import unicode_literals
from django.db import models
import re, datetime, bcrypt

#####	DATABASE MODELS

class UserManager(models.Manager):
	def validatorReg(self, userData):
		#	Checks form validity.
		errors = {}
		for key in userData:		#  Checks that all the forms have been filled out.  Adds error to the errors dictionary if found.
			if userData[key] == "":
				errors["emptyField"] = "Error: All forms must be filled out!"
				break
		errors.update(validName(userData["name"]))	#  Check validity of first name, add all errors found to the errors dictionary.
		errors.update(validName(userData["userName"]))		#  Check validity of email, add all errors found to the errors dictionary.
		errors.update(validPassword(userData["password1"]))	#  Check validity of password, add all errors found to the errors dictionary.
		if userData["password1"] != userData["password2"]:			#  Checks that the passwords match, adds error to the errors dictionary if found..
			errors["passMatch"] = "Error:  Confirmation password does not match!"
		if User.objects.filter(userName=userData['userName']).count() != 0:	#  Checks if the user is already registered.
			errors["register"] = "User already exists in database!"
		return errors
	def validatorLogin(self, postData):
		errors = {}
		userName = postData["userName"]
		userPassword = postData["password"]
		#	Check if the email is found in the database of registered users.
		if User.objects.filter(userName=userName).count() == 0:
			errors["login"] = "Error:  Invalid login info"
		else:
			user = User.objects.filter(userName=userName).first()
			hashedPW = user.passwordHash
			#	Check if the password matches the hashed password in the database.
			if not bcrypt.checkpw(userPassword.encode('utf-8'), hashedPW.encode('utf-8')):
				errors["login"] = "Error:  Invalid login info"
		return errors

class ItemManager(models.Manager):
	def validator(self, name):
		errors = {}
		if name == "":
			errors["emptyField"] = "Error: Item name must be filled out!"
			return errors
		if len(name) < 4:
			errors["nameLen"] = "Error:  Item's name is too short!  Name must be more than 3 characters."
		#	Checks if the object is already in the database.
		if Item.objects.filter(name=name).count() != 0:
			errors["register"] = "Item already exists in database!"
		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	userName = models.CharField(max_length=255)
	passwordHash = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Item(models.Model):
	name = models.CharField(max_length=255)
	added_by = models.ForeignKey(User, related_name="added_items")
	wished_adds = models.ManyToManyField(User, related_name="wished_items")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ItemManager()

#####  HELPER FUNCTIONS

def hasNumber(string):
	#	Helper function.  Checks if a string has a number in it.
	#	Input:  
	for char in string:
		if char.isnumeric():
			return True
	return False

def hasCap(string):
	#	Helper function.  Checks if a string has a capitalized letter in it.
	capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	for char in string:
		if char in capitals:
			return True
	return False

def validName(name):
	#	Helper function.  Checks if name is valid (only alphabetic letters and name length is 2 characters or more)
	#	Input:  String.  Either first name or last name.
	#	Output:  Dictionary of error messages.
	errors = {}
	if len(name) < 3:
		errors["nameLen"] = "Error: Name must be 3 or more characters long."
	return errors

def validPassword(password):
	#	Helper function.  Checks if email is valid (at least 1 capital letter, 1 number)
	#	Input:  String.  Password.
	#	Output:  Dictionary of error messages.
	errors = {}
	if len(password) < 8:
		errors["passLen"] = "Error: Password must be at least 8 characters long."
	if not hasNumber(password):
		errors["passNum"] = "Error: Password requires at least one number."
	if not hasCap(password):
		errors["passCap"] = "Error:  Password requires at least one capitalized letter."
	return errors
