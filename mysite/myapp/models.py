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
	joinKey = models.CharField(max_length=20)
	commissioner = models.ForeignKey(User,on_delete=models.CASCADE)
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

	def __str__(self):
		return self.teamName

class UnavailablePlayers(models.Model):
	playerID = models.IntegerField()
	league = models.ForeignKey(League, on_delete=models.CASCADE)


