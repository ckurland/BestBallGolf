import requests
import datetime


from . import keyStore




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

	if not is_cached:
		print("Not Cached Leaderboard")
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Leaderboard/%s?key=%s' % (str(tID), keyStore.key))
		request.session['leaderboard'] = response.json()

	leaderboard = request.session['leaderboard']
	return leaderboard


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
		tDate = datetime.datetime.strptime(t["StartDate"], '%Y-%m-%dT%H:%M:%S').date()
		#print("tDate: %s" % tDate)
		if tDate <= currentDate:
			prevTourney.append(t)

	return prevTourney





