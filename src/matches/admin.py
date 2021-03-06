from django.contrib import admin
from .models import Match


class MatchAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'percent']
    class Meta:
		model = Match

admin.site.register(Match, MatchAdmin)

