from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime
import requests
from . import keyStore

from . import models
from . import forms

from . import api


def home(request):

	context = {
			"title":"Best Ball",
			"opener":"Welcome to the Best Ball Golf Site",
			"initialStatement":"",
			"login":"/login/",
 			"logout":"/logout/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
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
				return redirect("/createTeam/"+str(new_leag.id)+"/")
		else:
			return redirect("/login/")
	else:
		form_instance = forms.LeagueForm()

	context = {
			"title":"Create League",
			"opener":"League Creation Zone",
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

	commish = None
	if request.user == instance.commissioner:
		commish = 1
	if 'end' in request.GET:
		instance.activeTourney = 0
		instance.save()
	print(instance.activeTourney)
	
	prevTourney = None
	curTourney = None
	endDate = None
	if instance.activeTourney == 0:
		if commish == 1:
			prevTourney = api.prevTourney(request)
	else:
		tour = api.prevTourney(request)
		for n in tour:
			if n["TournamentID"] == int(instance.tID):
				curTourney = n["Name"]
				break
		endDate = instance.endDate

	if 'tID' in request.GET:
		tID = request.GET['tID']
		instance.activeTourney = 1
		instance.activeDraft = 1

		for t in prevTourney:
			if t["TournamentID"] == int(tID):
				curTourney = t["Name"]
				endDate = datetime.datetime.strptime(t["EndDate"],'%Y-%m-%dT%H:%M:%S').date()
				print(curTourney)
				print(endDate)
				instance.tID = tID
				instance.endDate = endDate
				instance.save()
				break
		teams = models.Team.objects.filter(league=instance)
		for tm in teams:
			tm.player1 = None
			tm.player2 = None
			tm.player3 = None
			tm.player4 = None
			tm.curRound = 1
			tm.roundFin = 0
			tm.save()
		
		try:
			models.UnavailablePlayers.objects.filter(league=instance).delete()
		except:
			print("")
		prevTourney = None
		instance.save()

	draft = None
	if instance.activeDraft == 1:
		draft = 1


	context = {
			"title":"League Homepage",
			"opener":instance.leagueName +" Homepage",
			"initialStatement":instance.leagueDescription,
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+ str(instance_id)+"/",
			#"playersLeague":"/players/"+ str(instance_id)+"/",
			"myTeamLeague":"/myTeam/"+ str(team.id)+"/",
			"standingsLeague":"/standings/"+ str(team.id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeams":"/myTeams/",
			"tourneys":prevTourney,
			"curTourney":curTourney,
			"endDate":endDate,
			"commish":commish,
			"draft":draft,
			"team_id":team.id,
			"img":'media/'+str(instance.leagueImage),
	}
	return render(request, "league/home.html", context=context)

@login_required(login_url='/login/')
def leagueMyTeam(request,instance_id):

	prevTourney = api.prevTourney(request)
	#print(type(prevTourney[0]["TournamentID"]))

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

	swapEligible = None

	leaderboard = api.leaderboardCached(request,instance.league.tID)
	r = instance.curRound
	rounds = api.roundInfo(request,instance, r,leaderboard)
			

	if instance.league.activeTourney == 1:
		api.checkRound(request,instance_id,rounds,leaderboard)
		if api.roundDone(request,instance) == 1:
			swapEligible = 1
		curDate = datetime.datetime.now().date()
		rDate = None
		"""
		for p in leaderboard["Players"]:
			for ro in p["Rounds"]:
				if ro["Number"] == instance.curRound:
					rDate = datetime.datetime.strptime(ro["Day"], '%Y-%m-%dT%H:%M:%S').date()
					break
			break
		"""
		p = leaderboard["Tournament"]
		for ro in p["Rounds"]:
			if ro["Number"] == instance.curRound:
				rDate = datetime.datetime.strptime(ro["Day"], '%Y-%m-%dT%H:%M:%S').date()
				break
		if curDate < rDate:
			swapEligible = 1
		else:
			swapEligible = None
		print(curDate)
		print(rDate)

		r = instance.curRound
			
	totalHoleScore = api.thScore(rounds)

	totalScore = 0
	for t in range(18):
		totalScore += totalHoleScore[t]
	par = leaderboard["Tournament"]
	par = int(par["Par"])
	toPar = totalScore - par
	
	context = {
			"title":"My Team",
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+str(instance.league.id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeamLeague":"/myTeam/"+ str(instance_id)+"/",
			"standingsLeague":"/standings/"+ str(instance_id)+"/",
			"myTeams":"/myTeams/",
			"team_id":instance_id,
			"pAdd":pAdd,
			"team":team,
			"rounds":rounds,
			"tourneys":prevTourney,
			"curTourney":rounds["tName"],
			"curRound":r,
			"open":swapEligible,
			"totalHoleScore":totalHoleScore,
			"totalScore":totalScore,
			"toPar":toPar,
			"img":'media/'+str(instance.teamImage),
	}
	return render(request, "league/myTeam.html", context=context)

@login_required(login_url='/login/')
def leagueDraft(request,instance_id,player):
	#instance = models.League.objects.get(id=instance_id)
	instance = models.Team.objects.get(id=instance_id)
	#team = models.Team.objects.get(owner=request.user,league=instance)

	playerData = api.wgrCached(request)
	#playerData = api.playerCached(request)
	if 'pID' in request.GET:
		pID = request.GET['pID']
		if instance.player1 == None:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player1).delete()
			except:
				print("")
			instance.player1 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
			
		elif instance.player2 == None:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player2).delete()
			except:
				print("")
			instance.player2 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		elif instance.player3 == None:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player3).delete()
			except:
				print("")
			instance.player3 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		else:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player4).delete()
			except:
				print("")
			instance.player4 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		instance.save()

	if 'done' in request.GET:
		league = models.League.objects.get(id=instance.league.id)
		league.activeDraft = 0
		league.save()
		return redirect("/myTeam/"+str(instance_id)+"/")


	uPlayers = list(models.UnavailablePlayers.objects.filter(league=instance.league).values_list('playerID',flat=True))


	context = {
			"title":"Draft",
			"opener":"Draft",
			"initialStatement":"This is what separates the winners from the losers. Welcome to the draft.",
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+str(instance.league.id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeamLeague":"/myTeam/"+ str(instance_id)+"/",
			"standingsLeague":"/standings/"+ str(instance_id)+"/",
			"myTeams":"/myTeams/",
			"player":player,
			"uPlayers":uPlayers,
			"teamID":instance_id,
			"teamName":instance.teamName,
	}
	return render(request, "league/draft.html", context=context)

@login_required(login_url='/login/')
def addPlayer(request,teamID,pID):
	print("PLEASE WORK")
	instance = models.Team.objects.get(id=instance_id)
	if instance.player1 == None:
		try:
			models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player1).delete()
		except:
			print("")
		instance.player1 = pID
		p = models.UnavailablePlayers(playerID = pID,league=instance.league)
		p.save()
		
	elif instance.player2 == None:
		try:
			models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player2).delete()
		except:
			print("")
		instance.player2 = pID
		p = models.UnavailablePlayers(playerID = pID,league=instance.league)
		p.save()
	elif instance.player3 == None:
		try:
			models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player3).delete()
		except:
			print("")
		instance.player3 = pID
		p = models.UnavailablePlayers(playerID = pID,league=instance.league)
		p.save()
	else:
		try:
			models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player4).delete()
		except:
			print("")
		instance.player4 = pID
		p = models.UnavailablePlayers(playerID = pID,league=instance.league)
		p.save()
	instance.save()
	#return redirect("/myTeam/"+str(instance_id)+"/")
	return HttpResponse("Player Added")


@login_required(login_url='/login/')
def leaguePlayers(request,instance_id,player):
	instance = models.Team.objects.get(id=instance_id)

	playerData = api.wgrCached(request)
	if 'pID' in request.GET:
		pID = request.GET['pID']
		if int(player) == 1:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player1).delete()
			except:
				print("")
			instance.player1 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
			
		elif int(player) == 2:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player2).delete()
			except:
				print("")
			instance.player2 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		elif int(player) == 3:
			try:
				models.UnavailablePlayers.objects.get(league=instance.league,playerID=instance.player3).delete()
			except:
				print("")
			instance.player3 = pID
			p = models.UnavailablePlayers(playerID = pID,league=instance.league)
			p.save()
		else:
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


	context = {
			"title":"Players",
			"opener":"Players",
			"initialStatement":"Here are all of the available players",
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+str(instance.league.id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeamLeague":"/myTeam/"+ str(instance_id)+"/",
			"standingsLeague":"/standings/"+ str(instance_id)+"/",
			"myTeams":"/myTeams/",
			"player":player,
			"uPlayers":uPlayers,
			"teamID":instance_id,
			"teamName":instance.teamName,
	}
	return render(request, "league/players.html", context=context)

@login_required(login_url='/login/')
@csrf_exempt
def availPlayers_view(request,instance_id):
	if request.method == "GET":
		playerData = api.wgrCached(request)
		instance = models.Team.objects.get(id=instance_id)
		uPlayers = list(models.UnavailablePlayers.objects.filter(league=instance.league).values_list('playerID',flat=True))

		leaderboard = api.leaderboardCached(request,instance.league.tID)
		activePlayers = leaderboard["Players"]

		players_list = {"availPlayers":[]}
		for p in playerData:
			valid = 1
			for u in uPlayers:
				if p["PlayerID"] == u:
					valid = 0
			

			if valid == 1:
				for t in activePlayers:
					if t["PlayerID"] == p["PlayerID"]:
						players_list["availPlayers"] += [p]
						break
		return JsonResponse(players_list)
	else:
		return HttpResponse("Unsupported HTTP Method")

@login_required(login_url='/login/')
@csrf_exempt
def teamDraft_view(request,instance_id):
	if request.method == "GET":
		instance = models.Team.objects.get(id=instance_id)
		teams = models.Team.objects.filter(league=instance.league)
		team_list = {"teams":[]}
		for p in teams:
			if p.player1 is None:
				team_list["teams"] += [p.teamName]
		for p in reversed(teams):
			if p.player2 is None:
				team_list["teams"] += [p.teamName]
		for p in teams:
			if p.player3 is None:
				team_list["teams"] += [p.teamName]
		for p in reversed(teams):
			if p.player4 is None:
				team_list["teams"] += [p.teamName]
		return JsonResponse(team_list)
	else:
		return HttpResponse("Unsupported HTTP Method")


@login_required(login_url='/login/')
def leagueStandings(request,instance_id):

	prevTourney = api.prevTourney(request)

	instance = models.Team.objects.get(id=instance_id)
	stand = {
			"tourney":[]
			}
	teams = models.Team.objects.filter(league=instance.league)
	for to in prevTourney:
		vals = {
				"tName":to["Name"],
				"team":[],
				}
		work = 0
		for t in teams:
			try:
				score = models.Scores.objects.get(team=t,tID=to["TournamentID"])
				work += 1
				total = score.round1+score.round2+score.round3+score.round4
				total = total - (4 * score.coursePar)
				tval = {
						"name":t.teamName,
						"r1":score.round1-score.coursePar,
						"r2":score.round2-score.coursePar,
						"r3":score.round3-score.coursePar,
						"r4":score.round4-score.coursePar,
						"total":total,
						}
				vals["team"] += [tval]
			except:
				continue
		if work != 0:
			stand["tourney"] += [vals]
	
	context = {
			"title":"Standings",
			"initialStatement":"Here is where all of the league standings stuff will go.",
			"login":"/login/",
 			"logout":"/logout/",
			"league":"/leagueHome/"+str(instance.league.id)+"/",
 			"createLeague":"/createLeague/",
 			"joinLeague":"/joinLeague/",
			"myTeamLeague":"/myTeam/"+ str(instance_id)+"/",
			"standingsLeague":"/standings/"+ str(instance_id)+"/",
			"myTeams":"/myTeams/",
			"team_id":instance_id,
			"stand":stand,
	}
	return render(request, "league/standings.html", context=context)

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









