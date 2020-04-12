from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class Site(models.Model):
	playerList = JSONField()
	tournaments = JSONField()
	leaderboard = JSONField()
	wgr = JSONField()
	

class League(models.Model):
	leagueName = models.CharField(max_length=60)
	leagueDescription = models.CharField(max_length=500)
	joinKey = models.CharField(max_length=20,unique=True)
	commissioner = models.ForeignKey(User,on_delete=models.CASCADE)

	activeTourney = models.IntegerField(default = 0)
	activeDraft = models.IntegerField(default = 0)
	tID = models.IntegerField(null=True)
	endDate = models.DateField(null=True)

	leagueImage = models.ImageField(
		max_length=144,
		upload_to='uploads/%Y/%m/%d')
	
	
	def __str__(self):
		return self.leagueName
	
class Team(models.Model):
	teamName = models.CharField(max_length=20)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	league = models.ForeignKey(League, on_delete=models.CASCADE)
	teamImage = models.ImageField(
		max_length=144,
		upload_to='uploads/%Y/%m/%d')
	player1 = models.IntegerField(null=True)
	player2 = models.IntegerField(null=True)
	player3 = models.IntegerField(null=True)
	player4 = models.IntegerField(null=True)
	roundFin = models.IntegerField(default = 0) # 1 is round finished, 0 is not finished
	curRound = models.IntegerField(default = 1) 


	def __str__(self):
		return self.teamName

class UnavailablePlayers(models.Model):
	playerID = models.IntegerField()
	league = models.ForeignKey(League, on_delete=models.CASCADE)

"""
class CurTourney(models.Model):
	league = models.OneToOneField(League, on_delete=models.CASCADE)
	tID = models.IntegerField()
	endDate = models.DateField()
"""
	
class Scores(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	tID = models.IntegerField()
	coursePar = models.IntegerField(null=True)
	round1 = models.IntegerField(null=True)
	round2 = models.IntegerField(null=True)
	round3 = models.IntegerField(null=True)
	round4 = models.IntegerField(null=True)


