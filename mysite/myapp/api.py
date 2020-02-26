import requests


from . import keyStore




def playerCached(request):
	is_cached = ('playerData' in request.session)

	if not is_cached:
		print("Not Cached")
		response = requests.get('https://api.sportsdata.io/golf/v2/json/Players?key=%s' % keyStore.key)
		request.session['playerData'] = response.json()

	playerData = request.session['playerData']
	return playerData

def playerInfo(request,player_id):

	if player_id is None:
		return None
	players = playerCached(request)
	
	for p in players:
		if p["PlayerID"] == player_id:
			return p

	



