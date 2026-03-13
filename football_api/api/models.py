# football_api/api/models.py
from django.db import models


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    league = models.CharField(max_length=50, default='Unknown')
    country = models.CharField(max_length=50, default='Unknown')

    def __str__(self):
        return f"{self.name} ({self.league})"


class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    position = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.team})"


class Stats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='stats')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='player_stats')
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    shots = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)

    class Meta:
        unique_together = ('player', 'match')

    def __str__(self):
        return f"{self.player} stats for match {self.match.id}"