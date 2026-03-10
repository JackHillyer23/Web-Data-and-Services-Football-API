from rest_framework import serializers
from .models import Team, Player, Match, PlayerMatchStats


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class PlayerMatchStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMatchStats
        fields = '__all__'