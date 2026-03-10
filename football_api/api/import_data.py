# football_api/api/import_data.py
import os
import csv
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "football_api.settings")
django.setup()

from api.models import Team, Match, Player, Stats
from api.maps import league_map, country_map

# ✅ FIXED: removed '..' so path correctly resolves to api/data/final/
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'final')


def import_teams():
    with open(os.path.join(DATA_DIR, 'teams.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team_name = row['name'].strip()
            league = row.get('league', '').strip() or league_map.get(team_name, 'Unknown')
            country = row.get('country', '').strip() or country_map.get(team_name, 'Unknown')
            Team.objects.update_or_create(
                id=int(row['id']),
                defaults={
                    'name': team_name,
                    'league': league,
                    'country': country
                }
            )
    print("✅ Teams import complete.")


def import_matches():
    with open(os.path.join(DATA_DIR, 'matches.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            except ValueError:
                print(f"⚠️  Skipping invalid date: {row['date']}")
                continue
            try:
                home_team = Team.objects.get(id=int(row['home_team_id']))
                away_team = Team.objects.get(id=int(row['away_team_id']))
            except Team.DoesNotExist as e:
                print(f"⚠️  Skipping match id {row['id']}: {e}")
                continue
            Match.objects.update_or_create(
                id=int(row['id']),
                defaults={
                    'date': date,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': int(row['home_score']) if row['home_score'] else None,
                    'away_score': int(row['away_score']) if row['away_score'] else None,
                }
            )
    print("✅ Matches import complete.")


def import_players():
    with open(os.path.join(DATA_DIR, 'players.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                team = Team.objects.get(id=int(row['team_id']))
            except Team.DoesNotExist as e:
                print(f"⚠️  Skipping player id {row['id']}: {e}")
                continue
            Player.objects.update_or_create(
                id=int(row['id']),
                defaults={
                    'name': row['name'].strip(),
                    'team': team,
                    'position': row.get('position', '').strip(),
                    'nationality': row.get('nationality', '').strip(),
                }
            )
    print("✅ Players import complete.")


def import_stats():
    with open(os.path.join(DATA_DIR, 'stats.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            try:
                player = Player.objects.get(id=int(row['player_id']))
                match = Match.objects.get(id=int(row['match_id']))
            except (Player.DoesNotExist, Match.DoesNotExist) as e:
                print(f"⚠️  Skipping stat row {idx}: {e}")
                continue
            Stats.objects.update_or_create(
                # ✅ FIXED: stats.csv has no 'id' column, so we use player+match as the unique key
                player=player,
                match=match,
                defaults={
                    'goals': int(row.get('goals', 0) or 0),
                    'assists': int(row.get('assists', 0) or 0),
                    'minutes_played': int(row.get('minutes_played', 0) or 0),
                    'shots': int(row.get('shots', 0) or 0),
                    'yellow_cards': int(row.get('yellow_cards', 0) or 0),
                    'red_cards': int(row.get('red_cards', 0) or 0),
                }
            )
    print("✅ Stats import complete.")


if __name__ == "__main__":
    import_teams()
    import_matches()
    import_players()
    import_stats()
    print("🎉 All data imported successfully.")