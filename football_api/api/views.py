from rest_framework import viewsets
from .models import Team, Player, Match, PlayerMatchStats
from .serializers import TeamSerializer, PlayerSerializer, MatchSerializer, PlayerMatchStatsSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class PlayerMatchStatsViewSet(viewsets.ModelViewSet):
    queryset = PlayerMatchStats.objects.all()
    serializer_class = PlayerMatchStatsSerializer