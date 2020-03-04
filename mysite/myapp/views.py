from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import requests
from . import keyStore

from . import models
from . import forms

from . import api

"""
playerJson = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
playerData = response.json()
"""
	

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
	

	is_cached = ('playerData' in request.session)

	"""
	if not is_cached:
		print("Not Cached")
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
		request.session['playerData'] = response.json()

	playerData = request.session['playerData']
	"""
	playerData = api.playerCached(request)


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

	prevTourney = api.prevTourney(request)

	instance = models.Team.objects.get(id=instance_id)
	team = {
			"teamName":instance.teamName,
			"leagueID":instance.league.id,
			"teamImage":instance.teamImage,
			"player1":api.playerInfo(request,instance.player1),
			"player2":api.playerInfo(request,instance.player2),
			"player3":api.playerInfo(request,instance.player3),
			"player4":api.playerInfo(request,instance.player4),
			}
	pAdd = {
			"p1":"Swap",
			"p2":"Swap",
			"p3":"Swap",
			"p4":"Swap",
			}
	if team["player1"] is None:
		pAdd["p1"] = "Add"
	if team["player2"] is None:
		pAdd["p2"] = "Add"
	if team["player3"] is None:
		pAdd["p3"] = "Add"
	if team["player4"] is None:
		pAdd["p4"] = "Add"

	leaderboard = {}
	p1Round = {}
	p2Round = {}
	p3Round = {}
	p4Round = {}

	if 'tID' in request.GET:
		print("INNNNN")
		tID = request.GET['tID']
		leaderboard = leaderboardCached(request,tID)
		for p in leaderboard["Players"]:
			if p["PlayerID"] == instance.player1:
				for r in p["Rounds"]:
					print("PLEASE")
					if r["Number"] == 1:
						print("HELP")
						p1Round = r["Holes"]
			if p["PlayerID"] == instance.player2:
				for r in p["Rounds"]:
					if r["Number"] == 1:
						p2Round = r["Holes"]
			if p["PlayerID"] == instance.player3:
				for r in p["Rounds"]:
					if r["Number"] == 1:
						p3Round = r["Holes"]
			if p["PlayerID"] == instance.player4:
				for r in p["Rounds"]:
					if r["Number"] == 1:
						p4Round = r["Holes"]
	rounds = {
			"p1":p1Round,
			"p2":p2Round,
			"p3":p3Round,
			"p4":p4Round,
			}
	
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
			"pAdd":pAdd,
			"team":team,
			"rounds":rounds,
			"tourneys":prevTourney,
	}
	return render(request, "league/myTeam.html", context=context)

@login_required(login_url='/login/')
def leaguePlayers(request,instance_id,player,page=0):
	#instance = models.League.objects.get(id=instance_id)
	instance = models.Team.objects.get(id=instance_id)
	#team = models.Team.objects.get(owner=request.user,league=instance)

	playerData = api.playerCached(request)


	"""
	players = [{}]

	if 'first' in request.GET or 'last' in request.GET:
		first = request.GET['first']
		last = request.GET['last']
		for player in playerData:
			if player['FirstName'] == first or player['LastName'] == last:
				players += player
		playerData = players
	"""



	if 'pID' in request.GET:
		pID = request.GET['pID']
		if player == 1:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player1).delete()
			except:
				print("")
			instance.player1 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		
		if player == 2:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player2).delete()
			except:
				print("")
			instance.player2 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		if player == 3:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player3).delete()
			except:
				print("")
			instance.player3 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		if player == 4:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player4).delete()
			except:
				print("")
			instance.player4 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		instance.save()
		return redirect("/myTeam/"+str(instance_id)+"/")

	uPlayers = list(models.UnavailablePlayers.objects.filter(league=instance.league).values_list('playerID',flat=True))

	nextPage = page +1
	prevPage = page
	if page == 0:
		prevPage = 0
	else:
		prevPage = prevPage -1

	context = {
			"title":"Players",
			"opener":"Players",
			"initialStatement":"Here is where all of the available players will reside.",
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+str(instance.league.id)+"/",
			#"playersLeague":"/players/"+ str(instance_id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeamLeague":"/myTeam/"+ str(instance_id)+"/",
			"myTeams":"/myTeams/",
			"players":playerData[page*20:(page*20+20)],
			"page":page,
			"player":player,
			"uPlayers":uPlayers,
			"teamID":instance_id,
			"nextPage":"/players/"+str(instance_id)+"/"+str(player)+"/"+str(nextPage)+"/",
			"prevPage":"/players/"+str(instance_id)+"/"+str(player)+"/"+str(prevPage)+"/",
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









