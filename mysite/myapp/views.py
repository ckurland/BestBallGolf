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
playerJson = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
playerData = response.json()
"""

def playerCached(request):
	is_cached = ('playerData' in request.session)

	if not is_cached:
		print("Not Cached")
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
		request.session['playerData'] = response.json()

	playerData = request.session['playerData']
	return playerData
	

def home(request):

	"""
	siteJson = models.Site.objects.all().first()
	if siteJson is None:
		#playerJson = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
		pData = {"the":"one"}
		#pData = playerJson.json()
		st = models.Site(playerList = pData)
		st.save()
		siteJson = models.Site.objects.all().first()

	playerData = siteJson.playerList
	"""
	

	"""
	is_cached = ('playerData' in request.session)

	if not is_cached:
		print("Not Cached")
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
		request.session['playerData'] = response.json()

	playerData = request.session['playerData']
	"""
	playerData = playerCached(request)


	player = {}

	if 'first' in request.GET:
		if 'last' in request.GET:
			first = request.GET['first']
			last = request.GET['last']
			for players in playerData:
				if players['FirstName'] == first and players['LastName'] == last:
					player = players
					break


	context = {
			"title":"Best Ball",
			"opener":"Welcome to the Golf Best Ball Site",
			"initialStatement":" This is the beginnings of the best ball fantasy site",
			"login":"/login/",
 			"logout":"/logout/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
			"player":player,
			#"is_cached":is_cached,
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
			"leagueID":t_q.league.id,
			"teamImage":t_q.teamImage
			}]
		


	context = {
			"title":"My Teams",
			"opener":"My Teams",
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
			"teamList":teamList,
	}
	return render(request, "myTeams.html", context=context)

@login_required(login_url='/login/')
def leagueHome(request,instance_id):
	instance = models.League.objects.get(id=instance_id)
	team = models.Team.objects.get(owner=request.user,league=instance)


	context = {
			"title":"League Homepage",
			"opener":instance.leagueName +" Homepage",
			"initialStatement":instance.leagueDescription,
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+ str(instance_id)+"/",
			#"playersLeague":"/players/"+ str(instance_id)+"/",
			"myTeamLeague":"/myTeam/"+ str(team.id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
	}
	return render(request, "league/home.html", context=context)

@login_required(login_url='/login/')
def leagueMyTeam(request,instance_id):
	instance = models.Team.objects.get(id=instance_id)
	team = {
			"teamName":instance.teamName,
			"leagueID":instance.league.id,
			"teamImage":instance.teamImage,
			"player1":instance.player1,
			"player2":instance.player2,
			"player3":instance.player3,
			"player4":instance.player4,
			}
	pAdd = {
			"p1":"Swap",
			"p2":"Swap",
			"p3":"Swap",
			"p4":"Swap",
			}
	if team["player1"] is None:
		pAdd["p1"] = "Add"
	else:
		pAdd["p1"] = "Swap"
	if team["player2"] is None:
		pAdd["p2"] = "Add"
	else:
		pAdd["p2"] = "Swap"
	if team["player3"] is None:
		pAdd["p3"] = "Add"
	else:
		pAdd["p3"] = "Swap"
	if team["player4"] is None:
		pAdd["p4"] = "Add"
	else:
		pAdd["p4"] = "Swap"
		
	context = {
			"title":"My Team",
			"initialStatement":"Here is where all of the team stuff will go.",
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+str(instance.league.id)+"/",
			#"playersLeague":"/players/"+ str(instance.league.id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeamLeague":"/myTeam/"+ str(instance_id)+"/",
			"myTeams":"/myTeams/",
			"team_id":instance_id,
			"team":team,
	}
	return render(request, "league/myTeam.html", context=context)

@login_required(login_url='/login/')
def leaguePlayers(request,instance_id,player,page=0):
	#instance = models.League.objects.get(id=instance_id)
	instance = models.Team.objects.get(id=instance_id)
	#team = models.Team.objects.get(owner=request.user,league=instance)

	playerData = playerCached(request)

	if 'pID' in request.GET:
		pID = request.GET['pID']
		if player == 1:
			instance.player1 = pID
		if player == 2:
			instance.player2 = pID
		if player == 3:
			instance.player3 = pID
		if player == 4:
			instance.player4 = pID
		instance.save()
		return redirect("/myTeam/"+str(instance_id)+"/")

	context = {
			"title":"Players",
			"opener":"Players",
			"initialStatement":"Here is where all of the available players will reside.",
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+str(instance.league.id)+"/",
			"playersLeague":"/players/"+ str(instance_id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeamLeague":"/myTeam/"+ str(instance_id)+"/",
			"myTeams":"/myTeams/",
			"players":playerData[page*10:(page*10+10)],
	}
	return render(request, "league/players.html", context=context)




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









