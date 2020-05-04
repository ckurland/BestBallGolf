import requests
import datetime
import os
import json
import codecs


from . import keyStore
from . import models




def playerCached(request):
	is_cached = ('playerData' in request.session)

	if not is_cached:
		print("Not Cached Players")
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
		request.session['playerData'] = response.json()

	playerData = request.session['playerData']
	return playerData

def tourneyCached(request):
	is_cached = ('tourneyData' in request.session)

	if not is_cached:
		print("Not Cached Tourney")
		currentYear = str(datetime.datetime.now().year)
		print("Year: %s" % currentYear)
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Tournaments/%s?key=%s' % (currentYear, keyStore.key))
		request.session['tourneyData'] = response.json()

	tourneyData = request.session['tourneyData']
	return tourneyData

def leaderboardCached(request,tID):
	is_cached = ('leaderboard' in request.session)
	tourney_cached = ('tID' in request.session)

	#for testing
	path = os.path.dirname(os.path.abspath(__file__))
	path = path + '/full_tourney.json'
	f = codecs.open(path,'r','utf-8-sig')
	data = json.load(f)
	f.close()
	return data

	if tourney_cached:
		toID = request.session['tID']

	if not tourney_cached or str(toID) != str(tID) or not is_cached:
		print("Not Cached Leaderboard")
		print("Tourney ID: ",str(tID))
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Leaderboard/%s?key=%s' % (str(tID), keyStore.key))
		request.session['leaderboard'] = response.json()
		request.session['tID'] = tID

	leaderboard = request.session['leaderboard']
	return leaderboard

def wgrCached(request):
	is_cached = ('wgr' in request.session)

	if not is_cached:
		print("Not Cached WGR")
		currentYear = str(datetime.datetime.now().year)
		print("Year: %s" % currentYear)
		response = requests.get('https://api.sportsdata.io/golf/v2/json/PlayerSeasonStats/%s?key=%s' % (currentYear, keyStore.key))
		request.session['wgr'] = response.json()

	wgr = request.session['wgr']
	return wgr



def playerInfo(request,player_id):

	if player_id is None:
		return None
	#return player_id
	players = playerCached(request)
	
	for p in players:
		if p["PlayerID"] == player_id:
			return p
	

def prevTourney(request):
	tourneyData = tourneyCached(request)

	prevTourney = []
	
	for t in tourneyData:
		currentDate = datetime.datetime.now().date()
		#print("today Date: %s" % currentDate)
		tDate = datetime.datetime.strptime(t["EndDate"], '%Y-%m-%dT%H:%M:%S').date()
		#print("tDate: %s" % tDate)
		if tDate <= currentDate:
			prevTourney.append(t)

	return prevTourney


def thScore(rounds):

	totalHoleScore = [0] * 18

	count = 0;
	if rounds["p1"] is not None:
		for r in rounds["p1"]:
			totalHoleScore[count] = int(r["Score"])
			count += 1

	count = 0;
	if rounds["p2"] is not None:
		for r in rounds["p2"]:
			if int(r["Score"]) < totalHoleScore[count]:
				totalHoleScore[count] = int(r["Score"])
			count += 1
		
	count = 0;
	if rounds["p3"] is not None:
		for r in rounds["p3"]:
			if int(r["Score"]) < totalHoleScore[count]:
				totalHoleScore[count] = int(r["Score"])
			count += 1

	count = 0;
	if rounds["p4"] is not None:
		for r in rounds["p4"]:
			if int(r["Score"]) < totalHoleScore[count]:
				totalHoleScore[count] = int(r["Score"])
			count += 1

	return totalHoleScore


def roundInfo(request,instance,ro,leaderboard):
	tourney_cached = ('tID' in request.session)

	p1Round = None
	p2Round = None
	p3Round = None
	p4Round = None
	p1r = 0
	p2r = 0
	p3r = 0
	p4r = 0	

	tourneyName = None
	tID = None

	tourneyName = leaderboard["Tournament"]["Name"]
	for p in leaderboard["Players"]:
		if p["PlayerID"] == instance.player1:
			for r in p["Rounds"]:
				if r["Number"] == ro:
					p1r = r["Score"]
					p1Round = r["Holes"]
		if p["PlayerID"] == instance.player2:
			for r in p["Rounds"]:
				if r["Number"] == ro:
					p2r = r["Score"]
					p2Round = r["Holes"]
		if p["PlayerID"] == instance.player3:
			for r in p["Rounds"]:
				if r["Number"] == ro:
					p3r = r["Score"]
					p3Round = r["Holes"]
		if p["PlayerID"] == instance.player4:
			for r in p["Rounds"]:
				if r["Number"] == ro:
					p4r = r["Score"]
					p4Round = r["Holes"]

	rounds = {
			"p1":p1Round,
			"p2":p2Round,
			"p3":p3Round,
			"p4":p4Round,
			"t1":p1r,
			"t2":p2r,
			"t3":p3r,
			"t4":p4r,
			"tName":tourneyName,
			}
	return rounds


def checkRound(request,instance_id,rounds,leaderboard):
	instance = models.Team.objects.get(id=instance_id)
	tID = instance.league.tID
	curRound = int(instance.curRound)
	par = leaderboard["Tournament"]
	par = int(par["Par"])
	totalHoleScore = [0] * 18

	if instance.roundFin == 0:
		done = 0
		count = 0;
		if rounds["p1"] is not None:
			for r in rounds["p1"]:
				totalHoleScore[count] = int(r["Score"])
				count += 1
			if count == 18:
				done += 1
		count = 0;
		if rounds["p2"] is not None:
			for r in rounds["p2"]:
				if int(r["Score"]) < totalHoleScore[count]:
					totalHoleScore[count] = int(r["Score"])
				count += 1
			if count == 18:
				done += 1
		count = 0;
		if rounds["p3"] is not None:
			for r in rounds["p3"]:
				if int(r["Score"]) < totalHoleScore[count]:
					totalHoleScore[count] = int(r["Score"])
				count += 1
			if count == 18:
				done += 1
		count = 0;
		if rounds["p4"] is not None:
			for r in rounds["p4"]:
				if int(r["Score"]) < totalHoleScore[count]:
					totalHoleScore[count] = int(r["Score"])
				count += 1	
			if count >= 18:
				done += 1
		total = 0
		for i in range(18):
			total += totalHoleScore[i]	
		if done == 4:
			try:
				p = models.Scores.objects.get(team=instance,tID=tID)
				if curRound == 2:
					p.round2 = total
				elif curRound == 3:
					p.round3 = total
				else:
					p.round4 = total
				p.save()
			except:
				p = models.Scores(team = instance,tID = tID,coursePar=par,round1=total)
				p.save()
			instance.roundFin = 1
			instance.save()
			

def roundDone(request,instance):
	curRound = int(instance.curRound)

	teams = models.Team.objects.filter(league=instance.league)
	allDone = 1
	for t in teams:
		if t.roundFin == 0:
			allDone = 0
			break
	if allDone == 1:
		for t in teams:
			t.roundFin = 0
			if curRound < 4:
				t.curRound = curRound + 1
			else:
				t.league.activeTourney = 0
			t.save()

	return allDone
		
		



