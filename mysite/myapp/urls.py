from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_view),
    path('createLeague/', views.createLeague),
    path('myTeams/', views.myTeams),
    path('joinLeague/', views.joinLeague),
    path('createTeam/<int:instance_id>/', views.createTeam),
    path('leagueHome/<int:instance_id>/', views.leagueHome),
    path('myTeam/<int:instance_id>/', views.leagueMyTeam),
    path('players/<int:instance_id>/<int:player>/', views.leaguePlayers),
    path('draft/<int:instance_id>/<int:player>/', views.leagueDraft),
    path('standings/<int:instance_id>/', views.leagueStandings),
    path('register/', views.register),
	path('availPlayers/<int:instance_id>/', views.availPlayers_view),
	path('teamDraft/<int:instance_id>/', views.teamDraft_view),
    path('addPlayer/<int:instance_id>/<int:pID>/', views.addPlayer),
]
