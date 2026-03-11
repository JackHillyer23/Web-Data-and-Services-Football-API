from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Team, Player, Match, Stats
from .serializers import TeamSerializer, PlayerSerializer, MatchSerializer, StatsSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['league', 'country']
    search_fields = ['name']

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['team']
    search_fields = ['name']

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['home_team', 'away_team']
    search_fields = ['home_team__name', 'away_team__name']

class StatsViewSet(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['player', 'match']
    ordering_fields = ['goals', 'assists']