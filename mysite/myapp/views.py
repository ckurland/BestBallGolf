from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from . import keyStore

#from . import models
#from . import forms

response = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
playerData = response.json()
print("Lookup")

def home(request):

	"""  Attempt at caching the json
	is_cached = ('playerData' in request.session)

	if not is_cached:
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Player/%s?key=7a9a7e3dec8a4e19ba975c5dc65e978d' % '40000019')
		request.session['playerData'] = response.json()

	playerData = request.session['playerData']
	"""
	player = {}
	if 'first' in request.GET:
		if 'last' in request.GET:
			first = request.GET['first']
			last = request.GET['last']
			for players in playerData:
				if players['FirstName'] == first and players['LastName'] == last:
					player = players
					break

#	response = requests.get('https://api.sportsdata.io/golf/v2/json/Player/%s?key=7a9a7e3dec8a4e19ba975c5dc65e978d' % '40000019')
#	playerData = response.json()
	context = {
			"title":"Greetings",
			"opener":"Hello World",
			"initialStatement":" This is the beginnings of the best ball fantasy site",
			"test":"/test/",
			"login":"/login/",
 			"logout":"/logout/",
			"player":player,
	}
	return render(request, "home.html", context=context)
"""
"firstName":playerData['FirstName'],
"lastName":playerData['LastName'],
"playerID":playerData['PlayerID'],
"playerWeight":playerData['Weight'],
"""

def register(request):
	if request.method == "POST":
		form_instance = forms.RegistrationForm(request.POST)
		if form_instance.is_valid():
			form_instance.save()
			return redirect("/login/")
	else:
		form_instance = forms.RegistrationForm()
	context = {
		"form":form_instance,
		"login":"/login/",
	}
	return render(request, "registration/register.html", context=context)

def logout_view(request):
	logout(request)
	return redirect("/")









