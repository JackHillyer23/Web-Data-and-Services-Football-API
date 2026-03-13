from rest_framework import serializers
from .models import Team, Player, Match, Stats

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'league', 'country'] 

class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()  # human-readable team name

    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'nationality', 'team', 'team_name']

    def get_team_name(self, obj):
        return obj.team.name if obj.team else "Unknown"

class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.SerializerMethodField()
    away_team_name = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'home_team', 'away_team', 'date', 'home_team_name', 'away_team_name']

    def get_home_team_name(self, obj):
        return obj.home_team.name if obj.home_team else "Unknown"

    def get_away_team_name(self, obj):
        return obj.away_team.name if obj.away_team else "Unknown"

class StatsSerializer(serializers.ModelSerializer):
    player_name = serializers.SerializerMethodField()
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = Stats
        fields = ['id', 'player', 'match', 'goals', 'assists', 'player_name', 'match_info']

    def get_player_name(self, obj):
        return obj.player.name if obj.player else "Unknown"

    def get_match_info(self, obj):
        if obj.match:
            return f"{obj.match.home_team.name} vs {obj.match.away_team.name} on {obj.match.date}"
        return "Unknown"