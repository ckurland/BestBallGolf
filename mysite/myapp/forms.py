from django import forms
from django.core.validators import validate_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models



class LeagueForm(forms.Form):
	leagueName = forms.CharField(label="League Name",max_length=60)
	leagueDescription = forms.CharField(label="League Description", max_length=500)
	joinKey = forms.CharField(label="Join Key\n(for others to join your league)",max_length=20)
	leagueImage = forms.ImageField(label="League Picture",required=False)

	def save(self, request, commit=True):
		new_leag = models.League(
			leagueName = self.cleaned_data["leagueName"],
			leagueDescription = self.cleaned_data["leagueDescription"],
			joinKey = self.cleaned_data["joinKey"],
			commissioner = request.user,
			leagueImage = self.cleaned_data["leagueImage"]
		)
		if commit:
			new_leag.save()
		return new_leag

class TeamForm(forms.Form):
	teamName = forms.CharField(label="Team Name",max_length=60)
	teamImage = forms.ImageField(label="Team Picture",required=False)

	def save(self, request, leag_id, commit=True):
		leag = models.League.objects.get(id=leag_id)
		new_team = models.Team(
			teamName = self.cleaned_data["teamName"],
			owner = request.user,
			league = leag,
			teamImage = self.cleaned_data["teamImage"]
		)
		if commit:
			new_team.save()
		return new_team


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
        )

    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

