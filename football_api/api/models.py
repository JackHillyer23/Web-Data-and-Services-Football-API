from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    nationality = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Match(models.Model):
    date = models.DateField()
    season = models.CharField(max_length=20)
    home_team = models.ForeignKey(Team, related_name="home_matches", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_matches", on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"


class PlayerMatchStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    minutes_played = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    shots = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()