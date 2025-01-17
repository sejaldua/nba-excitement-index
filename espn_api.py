import requests
from pprint import pprint
import pandas as pd

# Define a function to get NBA game IDs for a specific date
def get_nba_game_ids(date):
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={date}"
    response = requests.get(url)
    data = response.json()
    # Extract game IDs
    games = data.get('events', [])
    game_ids = [game['id'] for game in games]
    return game_ids
# Example: Fetch game IDs for a single date
date = "20250113"  # Example date
game_ids = get_nba_game_ids(date)
print(game_ids)


# Fetch game IDs for multiple dates
from datetime import datetime, timedelta
start_date = datetime(2024, 10, 24)
end_date = datetime(2025, 1, 12)
current_date = start_date
all_game_ids = []
while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    game_ids = get_nba_game_ids(date_str)
    all_game_ids.extend(game_ids)
    current_date += timedelta(days=1)
    break
# Print all game IDs

# Function to fetch win probability data for a game
def get_win_probability(game_id):
    url = f"https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events/{game_id}/competitions/{game_id}/plays/"
    response = requests.get(url)
    data = response.json()
    # Extract win probability data
    home_wp = []
    pages = data['pageCount']
    for i in range(pages):
        url = f"https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events/{game_id}/competitions/{game_id}/plays?page={i+1}"
        response = requests.get(url)
        data = response.json()
        for wp in data['items']:
            probability = requests.get(wp['probability']['$ref']).json()
            home_wp.append(
                {
                    'id': wp['id'],
                    'sequence': wp['sequenceNumber'], 
                    'period': wp['period']['number'],
                    'clock': wp['clock']['displayValue'],
                    'play_type': wp['type']['text'],
                    'text': wp['text'],
                    'alternative_text': wp['alternativeText'],
                    'probability': probability['homeWinPercentage'],
                    'away_score': wp['awayScore'],
                    'home_score': wp['homeScore'],
                })
        # win_probabilities.append({
        #     'time': wp.get('play', {}).get('clock', 'Unknown'),
        #     'team': wp.get('team', {}).get('id', 'Unknown'),
        #     'probability': wp.get('value', 0)  # Value ranges between 0 and 1
        # })
    return home_wp

print(len(all_game_ids))
for gid in all_game_ids:
    win_probabilities = get_win_probability(gid)
    pprint(win_probabilities)
    print(len(win_probabilities))
    df = pd.DataFrame.from_records(win_probabilities)
    break

print(df)
