from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from . models import User
import re, datetime, bcrypt

# Create your views here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.

def index(request):
	return render(request, "login_registration/index.html")

def success(request):
	if "userID" not in request.session:
		messages.error(request, "You are not logged in.")
		return redirect("/")
	else:
		return render(request, "login_registration/success.html")

def register(request):
	#	Executed when the registration form is submitted.
	userData = retrieveForms(request)
	errors = User.objects.validatorReg(userData)
	#	If any errors are found, store the errors as messages & redirect to root.
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	#	If user is not in the database & all the forms are valid, create a new user with the hashed password and store on server database.
	else:
		password = userData['password1']
		hashedPW = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		User.objects.create(first_name=userData['firstName'], last_name=userData['lastName'], email=userData['email'], passwordHash=hashedPW)
		messages.info(request, "You have successfully registered")
		return redirect('/')

def login(request):
	errors = User.objects.validatorLogin(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		#	If passwords match, flash a successful login message and redirect to success route.
		user = User.objects.filter(email=request.POST["email"]).first()
		request.session["userID"] = user.id
		messages.info(request, "You have successfully logged in!  Welcome back, " + user.first_name + "!")
		return redirect("/success")

def logout(request):
	request.session.pop("userID")
	return redirect('/')


##### HELPER FUNCTIONS

def retrieveForms(request):
	# Returns a dictionary of the fields' names as keys and the fields' values (from registration/login page) as values.
	data = { }
	keys = ['firstName', 'lastName', 'email', 'password1', 'password2']
	for key in keys:
		data[key] = request.POST[key]
	return data

