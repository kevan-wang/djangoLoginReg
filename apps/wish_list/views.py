from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from . models import User, Item
import re, datetime, bcrypt


#####		LOGIN & REGISTRATION VIEWS

def index(request):
	return render(request, "wish_list/index.html")

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
		User.objects.create(name=userData['name'], userName=userData['userName'], passwordHash=hashedPW)
		messages.info(request, "You have successfully registered")
		return redirect('/')

def login(request):
	errors = User.objects.validatorLogin(request.POST)
	#	If any errors are found, store the errors as messages & redirect to root.
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		#	If passwords match, flash a successful login message and redirect to dashboard.
		user = User.objects.filter(userName=request.POST["userName"]).first()
		#	Confirmation of login is the user's ID number stored in the session.
		request.session["userID"] = user.id
		messages.info(request, "You have successfully logged in!  Welcome back, " + user.userName + "!")
		return redirect("/dashboard")

def logout(request):
	#	Logging out removes he user's ID from session.
	request.session.pop("userID")
	messages.error(request, "You have logged out.")
	return redirect('/')


#####		DASHBOARD & WISHLIST VIEWS

def dashboard(request):
	#	Renders the dashboard.
	if "userID" not in request.session:		#	Security feature:  This process will not execute without an authentic login.
		messages.error(request, "You are not logged in.")
		return redirect("/")
	else:
		context = {
			"userName" : User.objects.get(id=request.session["userID"]).userName,
			"myWishList" : Item.objects.filter(wished_adds=User.objects.get(id=request.session["userID"])),
			"items" : Item.objects.exclude(added_by=User.objects.get(id=request.session["userID"]))
		}
		return render(request, "wish_list/dashboard.html", context)

def showItem(request, id):
	#	Renders the  item's individual page, showing stats of an individual item.
	if "userID" not in request.session:		#	Security feature:  This process will not execute without an authentic login.
		messages.error(request, "You are not logged in.")
		return redirect("/")
	else:
		context = {
			"item" : Item.objects.get(id=id),
			"users" : Item.objects.get(id=id).wished_adds.all()
		}
		return render(request, "wish_list/showItem.html", context)

def create(request):
	#	Renders the "Create a new item" page.
	if "userID" not in request.session:		#	Security feature:  This process will not execute without an authentic login.
		messages.error(request, "You are not logged in.")
		return redirect("/")
	else:
		return render(request, "wish_list/newItem.html")

def createItem(request):
	#	POST method.  Executed through /create_item route from the wish_items/create route (newItem.html)
	if "userID" not in request.session:		#	Security feature:  This process will not execute without an authentic login.
		messages.error(request, "You are not logged in.")
		return redirect("/")
	else:
		itemName = request.POST["itemName"]
		itemName = itemName.replace(" ", "_")		#	String editing necessary:  Could not store the name properly without this.  Fix later. 
		errors = Item.objects.validator(itemName)
		#	Error display.
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/wish_items/create')
		else:
			#	Add the item to the database and add it to the user's wishlist.
			user = User.objects.get(id=request.session["userID"])
			item = Item(name=itemName, added_by=user)		
			item.save()
			item.wished_adds.add(user)
			messages.info(request, "Successfully added new item!")
			return redirect('/dashboard')

def addWish(request):
	#	POST method.  Executed through /add_wish route from the /dashboard route (dashboard.html)
	if "userID" not in request.session:		#	Security feature:  This process will not execute without an authentic login.
		messages.error(request, "You are not logged in.")
		return redirect("/")
	else:
		#	Adding the item to the user's wishlist.
		itemName = request.POST["itemName"]
		item = Item.objects.get(name=itemName)
		user = User.objects.get(id=request.session["userID"])
		#	If item is already on the user's wishlist, add a message indicating such.
		if item in Item.objects.filter(wished_adds=user):
			messages.error(request, "This is already in your wish list!")
			return redirect('/dashboard')
		user = User.objects.get(id=request.session["userID"])
		item.wished_adds.add(user)
		return redirect('/dashboard')

def remove(request):
	#	POST method.  Executed through /remove route from the /dashboard route (dashboard.html)
	if "userID" not in request.session:		#	Security feature:  This process will not execute without an authentic login.
		messages.error(request, "You are not logged in.")
		return redirect("/")
	else:
		#	Removes the logged in user from the item's wished_adds attribute.
		#	Remove button only appears for the user who wished it when they are logged in.
		itemName = request.POST["itemName"]
		item = Item.objects.get(name=itemName)
		user = User.objects.get(id=request.session["userID"])
		item.wished_adds.remove	(user)
		messages.info(request, "Item has been removed from your wishlist.")
		return redirect('/dashboard')

def delete(request):
	#	POST method.  Executed through /delete route from the /dashboard route (dashboard.html)
	if "userID" not in request.session:		#	Security feature:  This process will not execute without an authentic login.
		messages.error(request, "You are not logged in.")
		return redirect("/")
	else:
		#	Deletes the item from the database.
		#	Delete button only appears for the user who added it when they are logged in.
		itemName = request.POST["itemName"]
		item = Item.objects.get(name=itemName)
		item.delete()
		messages.info(request, "Item has been deleted.")
		return redirect('/dashboard')



#####		HELPER FUNCTIONS

def retrieveForms(request):
	# Returns a dictionary of the fields' names as keys and the fields' values (from registration/login page) as values.
	data = { }
	keys = ['name', 'userName', 'password1', 'password2']
	for key in keys:
		data[key] = request.POST[key]
	return data

