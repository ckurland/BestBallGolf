from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import requests
from . import keyStore

from . import models
from . import forms

"""
response = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
playerData = response.json()
print("Lookup")
"""

def home(request):

	is_cached = ('playerData' in request.session)

	"""
	if not is_cached:
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
		request.session['playerData'] = response.json()

	playerData = request.session['playerData']
	player = {}
	if 'first' in request.GET:
		if 'last' in request.GET:
			first = request.GET['first']
			last = request.GET['last']
			for players in playerData:
				if players['FirstName'] == first and players['LastName'] == last:
					player = players
					break
	"""
	context = {
			"title":"Best Ball",
			"opener":"Welcome to the Golf Best Ball Site",
			"initialStatement":" This is the beginnings of the best ball fantasy site",
			"login":"/login/",
 			"logout":"/logout/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
			#"player":player,
			"is_cached":is_cached,
	}
	return render(request, "home.html", context=context)

@login_required(login_url='/login/')
def joinLeague(request):

	if 'joinKey' in request.GET:
		joinKey = request.GET['joinKey']
		instance = models.League.objects.get(joinKey=joinKey)
		# do error checking to make sure instance is not DoesNotExist
		return redirect("/createTeam/"+str(instance.id)+"/")


	context = {
			"title":"Join League",
			"opener":"Join a League",
			"login":"/login/",
 			"logout":"/logout/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
	}
	return render(request, "joinLeague.html", context=context)

@login_required(login_url='/login/')
def createLeague(request):
	if request.method == "POST":
		if request.user.is_authenticated:
			form_instance = forms.LeagueForm(request.POST,request.FILES)
			if form_instance.is_valid():
				new_leag = form_instance.save(request=request)
				return redirect("/")
		else:
			return redirect("/")
	else:
		form_instance = forms.LeagueForm()

	context = {
			"title":"Create League",
			"opener":"League creation zone",
			"initialStatement":"Create your league!!",
			"login":"/login/",
 			"logout":"/logout/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
			"form":form_instance,
	}
	return render(request, "createLeague.html", context=context)

@login_required(login_url='/login/')
def createTeam(request,instance_id):
	if request.method == "POST":
		if request.user.is_authenticated:
			form_instance = forms.TeamForm(request.POST,request.FILES)
			if form_instance.is_valid():
				new_team = form_instance.save(request=request,leag_id=instance_id)
				return redirect("/")
		else:
			return redirect("/")
	else:
		form_instance = forms.TeamForm()

	context = {
			"title":"Create Team",
			"opener":"Team Creation Zone",
			"initialStatement":"Create your Team!!",
			"login":"/login/",
 			"logout":"/logout/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
			"form":form_instance,
			"leag_id":instance_id,
	}
	return render(request, "createTeam.html", context=context)

@login_required(login_url='/login/')
def myTeams(request):

	teamList = []
	if request.user.is_authenticated:
		teamQuery = models.Team.objects.filter(owner=request.user)
		for t_q in teamQuery:
			#leag = models.League.objects.get(id=t_q.league)
			teamList += [{
			"teamName":t_q.teamName,
			"leagueName":t_q.league.leagueName,
			"teamImage":t_q.teamImage
			}]
		


	context = {
			"title":"My Teams",
			"opener":"My Teams",
			"login":"/login/",
 			"logout":"/logout/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
			"teamList":teamList,
	}
	return render(request, "myTeams.html", context=context)


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









