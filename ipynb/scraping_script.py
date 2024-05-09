# Imports
import datetime
import requests
import time
import numpy as np
import traceback
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()


# Control structure loop variables
is_reached_end = False
count = 0
today = datetime.datetime.now()
endpoints = list()
data = list()
loaded_requests = 0
total_count = 0
TOTAL_DATA_REQUIRED = 5000


# Gets the matches from the football API.
def get_matches(url):
  response = requests.get(url,
                    headers={'X-Unfold-Lineups': "true",
                             'X-Unfold-Goals': "true",
                             'X-Auth-Token': os.environ["FOOTBALL_DATA_API_KEY"]})
  if response.status_code == 200:
    return response.json()["matches"]
  else:
    print(response.text)
    return []

# Gets a single match for more information
def get_match(id):
  response = requests.get(f'https://api.football-data.org/v4/matches/{id}',
                    headers={'X-Unfold-Lineups': "true",
                             'X-Unfold-Goals': "true",
                             'X-Auth-Token': os.environ["FOOTBALL_DATA_API_KEY"]})
  if response.status_code == 200:
    return response.json()
  else:
    print(response.text)
    return None

while is_reached_end == False:
  try:
    timedelta = datetime.timedelta(days=10)
    past_ten_days = today - timedelta
    endpoint = f"https://api.football-data.org/v4/matches?competitions=PL&dateTo={today.strftime('%Y-%m-%d')}&dateFrom={past_ten_days.strftime('%Y-%m-%d')}"

    if loaded_requests == 10:
        print(f'Requests: {loaded_requests}, sleeping.')
        time.sleep(60)
        print(f'Reset, continue.')
        loaded_requests = 0

    matches = get_matches(endpoint)
    print(f"Loaded: {len(matches)} matches. Date: {today} - {past_ten_days}.")
    loaded_requests += 1

    if matches:
        for match_ in matches:
            # API free account allows 10 requests per 60 seconds.
            if loaded_requests == 10:
                print(f'Requests: {loaded_requests}, sleeping.')
                time.sleep(60)
                print(f'Reset, continue.')
                loaded_requests = 0

            match_id = match_['id']
            match_ = get_match(match_["id"])
            print(f"{match_id}: {match_}")
            loaded_requests += 1 # matches request = +1

            if match_ is not None:
                data.append([
                    match_["id"],
                    match_["utcDate"], # date
                    match_["status"], # status
                    match_["competition"]["name"], # league_name
                    match_["competition"]["id"], # league_id
                    match_["competition"]["type"], # league_type
                    match_["stage"], # stage
                    match_["homeTeam"]["shortName"], # home_name
                    match_["homeTeam"]["id"], # home_id
                    match_["awayTeam"]["shortName"], # away_name
                    match_["awayTeam"]["id"], # away_id
                    match_["venue"], # venue
                    match_["score"]["halfTime"]["home"], # score_home_ht
                    match_["score"]["halfTime"]["away"], # score_away_ht
                    match_["score"]["fullTime"]["home"], # score_home_ft
                    match_["score"]["fullTime"]["away"], # score_away_ft
                    match_["odds"]["homeWin"], # home_odds
                    match_["odds"]["draw"], # draw_odds
                    match_["odds"]["awayWin"] # away_odds
                ])
                
                total_count += 1 # match request = +9, total = 10, then loop resets back to 0.
                print(f'Progressive percentage: {total_count} ({round((total_count/TOTAL_DATA_REQUIRED)*100, 2)}%)')

    # End while loop when required sample size has been reached.
    if (total_count == TOTAL_DATA_REQUIRED):
        is_reached_end = True
        break
    else:
        # Else keep the while loop running.
        today = past_ten_days

  except:
    print(traceback.format_exc())

    # Incase something goes wrong with the above script, save current progress.
    df = pd.DataFrame(data, columns=["id", "date", "status", "league_name", "league_id", "league_type", "stage", "home_team", "home_team_id", "away_team", "away_team_id", "venue", "score_home_ht", "score_away_ht", "score_home_ft", "score_away_ft", "home_odds", "draw_odds", "away_odds"])
    df.to_csv(f"./datasets/data_premier_league_{total_count}.csv", index=False)
        
    # Await the next 60 seconds to be allowed to request more data, incase limit has been reached.
    time.sleep(60)
    continue

df = pd.DataFrame(data, columns=["id", "date", "status", "league_name", "league_id", "league_type", "stage", "home_team", "home_team_id", "away_team", "away_team_id", "venue", "score_home_ht", "score_away_ht", "score_home_ft", "score_away_ft", "home_odds", "draw_odds", "away_odds"])
df.to_csv(f"./datasets/data_premier_league.csv", index=False)