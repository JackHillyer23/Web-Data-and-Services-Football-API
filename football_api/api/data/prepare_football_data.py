import pandas as pd
import os
import random
from datetime import datetime

# Paths
RAW_DIR = os.path.join(os.path.dirname(__file__), 'raw')
FINAL_DIR = os.path.join(os.path.dirname(__file__), 'final')
os.makedirs(FINAL_DIR, exist_ok=True)

# --------------------------
# 1️⃣ Canonical team mapping
# --------------------------

# League & country mapping
league_map = {
    # Premier League (England)
    "Manchester United": "Premier League",
    "Liverpool": "Premier League",
    "Chelsea": "Premier League",
    "Arsenal": "Premier League",
    "Aston Villa": "Premier League",
    "Man City": "Premier League",
    "Brentford": "Premier League",
    "Tottenham": "Premier League",
    "Brighton": "Premier League",
    "Newcastle": "Premier League",
    "Fulham": "Premier League",
    "Crystal Palace": "Premier League",
    "Everton": "Premier League",
    "Sunderland": "Premier League",
    "West Ham": "Premier League",
    "Wolves": "Premier League",
    "Leeds": "Premier League",
    "Bournemouth": "Premier League",
    "Burnley": "Premier League",
    "Forest": "Premier League",
    
    # La Liga (Spain)
    "Barcelona": "La Liga",
    "Real Madrid": "La Liga",
    "Atletico Madrid": "La Liga",
    "Villarreal": "La Liga",
    "Real Betis": "La Liga",
    "Celta Vigo": "La Liga",
    "Espanyol": "La Liga",
    "Real Sociedad": "La Liga",
    "Getafe": "La Liga",
    "Athletic Bilbao": "La Liga",
    "Osasuna": "La Liga",
    "Valencia": "La Liga",
    "Rayo Vallecano": "La Liga",
    "Sevilla": "La Liga",
    "Girona": "La Liga",
    "Alaves": "La Liga",
    "Elche": "La Liga",
    "Mallorca": "La Liga",
    "Levante": "La Liga",
    "Oviedo": "La Liga",
    
    # Serie A (Italy)
    "Inter": "Serie A",
    "Milan": "Serie A",
    "Napoli": "Serie A",
    "Como": "Serie A",
    "Roma": "Serie A",
    "Juventus": "Serie A",
    "Atalanta": "Serie A",
    "Bologna": "Serie A",
    "Sassuolo": "Serie A",
    "Lazio": "Serie A",
    "Udinese": "Serie A",
    "Parma Calcio": "Serie A",
    "Genoa": "Serie A",
    "Cagliari": "Serie A",
    "Torino": "Serie A",
    "Lecce": "Serie A",
    "Fiorentina": "Serie A",
    "Cremonese": "Serie A",
    "Hellas Verona": "Serie A",
    "Pisa": "Serie A",
    
    # Bundesliga (Germany)
    "Bayern Munich": "Bundesliga",
    "Borussia Dortmund": "Bundesliga",
    "TSG Hoffenheim": "Bundesliga",
    "Stuttgart": "Bundesliga",
    "RB Leipzig": "Bundesliga",
    "Bayer Leverkusen": "Bundesliga",
    "Eintracht Frankfurt": "Bundesliga",
    "SC Freiburg": "Bundesliga",
    "FC Augsburg": "Bundesliga",
    "Hamburger SV": "Bundesliga",
    "Union Berlin": "Bundesliga",
    "Borussia Mönchengladbach": "Bundesliga",
    "Werder Bremen": "Bundesliga",
    "1. FC Cologne": "Bundesliga",
    "Mainz 05": "Bundesliga",
    "FC St. Pauli": "Bundesliga",
    "VfL Wolfsburg": "Bundesliga",
    "1. FC Heidenheim": "Bundesliga",
    
    # Ligue 1 (France)
    "PSG": "Ligue 1",
    "Lens": "Ligue 1",
    "Marseille": "Ligue 1",
    "Lyon": "Ligue 1",
    "Stade Rennais": "Ligue 1",
    "Lille": "Ligue 1",
    "Monaco": "Ligue 1",
    "Strasbourg Alsace": "Ligue 1",
    "Stade Brest 29": "Ligue 1",
    "Lorient": "Ligue 1",
    "Angers": "Ligue 1",
    "Toulouse": "Ligue 1",
    "Paris": "Ligue 1",
    "Le Havre": "Ligue 1",
    "Nice": "Ligue 1",
    "Auxerre": "Ligue 1",
    "Nantes": "Ligue 1",
    "Metz": "Ligue 1",
}

# Country mapping
country_map = {
    **{team: "England" for team in league_map if league_map[team]=="Premier League"},
    **{team: "Spain" for team in league_map if league_map[team]=="La Liga"},
    **{team: "Italy" for team in league_map if league_map[team]=="Serie A"},
    **{team: "Germany" for team in league_map if league_map[team]=="Bundesliga"},
    **{team: "France" for team in league_map if league_map[team]=="Ligue 1"},
}

# --------------------------
# 2️⃣ CSV name corrections
# --------------------------
team_name_corrections = {
    "M'gladbach": "Borussia Mönchengladbach",
    "Ath Madrid": "Atletico Madrid",
    "Ein Frankfurt": "Eintracht Frankfurt",
    "Nott'm Forest": "Forest",
    "Espanol": "Espanyol",
    "Vallecano": "Rayo Vallecano",
    "Ath Bilbao": "Athletic Bilbao",
    "FC Koln": "1. FC Cologne",
    "St Pauli": "FC St. Pauli",
    "Paris SG": "Paris FC",
    "Man United": "Manchester United",
    "Heidenheim": "1. FC Heidenheim",
    "Verona": "Hellas Verona",
    "Parma": "Parma Calcio",
    "Borussia Dortmund": "Dortmund",
    "FC Augsburg": "Augsburg",
    "Stade Rennais": "Rennes",
    "Bayer Leverkusen": "Leverkusen",
    "Strasbourg Alsace": "Strasbourg",
    "Real Sociedad": "Sociedad",
    "Real Betis": "Betis",
    "Celta Vigo": "Celta",
    "SC Freiburg": "Freiburg",
    "TSG Hoffenheim": "Hoffenheim",
    "Stade Brest 29": "Brest",
    "Hamburger SV": "Hamburg",
    "Mainz 05": "Mainz",


}

# --------------------------
# 3️⃣ Read league CSVs
# --------------------------
league_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv')]
matches_all = []
teams_set = set()

for file in league_files:
    df = pd.read_csv(os.path.join(RAW_DIR, file))
    for _, row in df.iterrows():
        home_team = team_name_corrections.get(row['HomeTeam'], row['HomeTeam'])
        away_team = team_name_corrections.get(row['AwayTeam'], row['AwayTeam'])
        season = row.get('Season', '2025/26')
        raw_date = row['Date']

        # Convert date to YYYY-MM-DD
        try:
            date_obj = datetime.strptime(raw_date, "%d/%m/%y")
            date_str = date_obj.strftime("%Y-%m-%d")
        except:
            date_str = "2025-01-01"

        home_score = row['FTHG'] if 'FTHG' in row else row.get('HomeScore', 0)
        away_score = row['FTAG'] if 'FTAG' in row else row.get('AwayScore', 0)

        teams_set.add(home_team)
        teams_set.add(away_team)

        matches_all.append({
            'date': date_str,
            'season': season,
            'home_team': home_team,
            'away_team': away_team,
            'home_score': home_score,
            'away_score': away_score
        })

# --------------------------
# 4️⃣ Create teams.csv
# --------------------------
teams = list(teams_set)
teams_csv = []
for idx, team_name in enumerate(teams, start=1):
    teams_csv.append({
        'id': idx,
        'name': team_name,
        'league': league_map.get(team_name, 'Unknown'),
        'country': country_map.get(team_name, 'Unknown')
    })

teams_df = pd.DataFrame(teams_csv)
teams_df.to_csv(os.path.join(FINAL_DIR, 'teams.csv'), index=False)

# Map team names to IDs
team_id_map = {team['name']: team['id'] for team in teams_csv}

# --------------------------
# 5️⃣ Create matches.csv
# --------------------------
matches_csv = []
for idx, match in enumerate(matches_all, start=1):
    matches_csv.append({
        'id': idx,
        'date': match['date'],
        'season': match['season'],
        'home_team_id': team_id_map[match['home_team']],
        'away_team_id': team_id_map[match['away_team']],
        'home_score': match['home_score'],
        'away_score': match['away_score']
    })

matches_df = pd.DataFrame(matches_csv)
matches_df.to_csv(os.path.join(FINAL_DIR, 'matches.csv'), index=False)

# --------------------------
# 6️⃣ Create players.csv
# --------------------------
players_csv = []
player_id = 1
positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']

for team in teams_csv:
    for i in range(20):
        players_csv.append({
            'id': player_id,
            'name': f'Player {player_id}',
            'age': random.randint(18, 35),
            'nationality': 'Unknown',
            'position': random.choice(positions),
            'team_id': team['id']
        })
        player_id += 1

players_df = pd.DataFrame(players_csv)
players_df.to_csv(os.path.join(FINAL_DIR, 'players.csv'), index=False)

# --------------------------
# 7️⃣ Create stats.csv
# --------------------------
stats_csv = []
for match in matches_csv:
    for player in players_csv:
        if player['team_id'] not in [match['home_team_id'], match['away_team_id']]:
            continue
        stats_csv.append({
            'player_id': player['id'],
            'match_id': match['id'],
            'minutes_played': random.randint(0, 90),
            'goals': random.randint(0, 3),
            'assists': random.randint(0, 2),
            'shots': random.randint(0, 5),
            'yellow_cards': random.randint(0, 1),
            'red_cards': 0
        })

stats_df = pd.DataFrame(stats_csv)
stats_df.to_csv(os.path.join(FINAL_DIR, 'stats.csv'), index=False)

print("All CSVs generated in api/data/final/ with corrected leagues and countries")