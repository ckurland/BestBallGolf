from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Site)
admin.site.register(models.League)
admin.site.register(models.Team)
admin.site.register(models.UnavailablePlayers)

