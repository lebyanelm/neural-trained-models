# Imports
import datetime
import requests
import time
import random
import numpy as np
import traceback
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()


API_KEYS = [
   # KEY, No. REQUESTS MADE, LAST REQ. TIMESTAMP
   ["9ff4b5192f4b4272855493db973d8c61", 0, None],
   ["a151d6c3003c4f838ffa519bea3315a1", 0, None],
   ["618a74d05cfb4401b7a66d4ed4c3cae5", 0, None],
   ["f8024b296b70487c852eff7a353d8f85", 0, None],
   ["024b012d8df24b3b9ee70863633e0fcc", 0, None],
   ["1a65d4d0d7cc4f5893b438b4092da912", 0, None],
   ["c872982f9423441fbfab53d52c8558b4", 0, None],
   ["bd8c94c0ce6e435d8ddc6f3d0d2ba0aa", 0, None],
   ["5433c517fdf0408da4578b14bd95b74b", 0, None],
   ["be9ee655916a465895ccd17f3026422a", 0, None],
   ["61659ea176ba454f98a421ec6facaa3d", 0, None],
   ["9cd7992817f04d5abfbe6ffa02624d6d", 0, None],
   ["3fab499119a547f1abf56b83db88ca1b", 0, None],
   ["ec75a3fc37c1403db385c598e3cef779", 0, None],
   ["2bb6d52219664b18b5efde63d075a03b", 0, None],
   ["9b648751e85443f1bde592d4b337b7e1", 0, None],
   ["2819b51d87214f98a21bbff55bb6b4d4", 0, None],
   ["611db8b59ba244d6bab7fc71b8d23ac9", 0, None],
   ["cce392b8fca641f3a41361756a3cd36b", 0, None],
   ["542f193f142d42a5845ffda13c60b705", 0, None],
   ["8ff44d4142974404875bb5ecb71eba25", 0, None],
   ["ba93366e933a43e4b2f0ffe2f32c17a7", 0, None],
   ["3aa9fa11915b4ff595ccd91cc75834fd", 0, None],
   ["92eecef75959449e84abb7559a2f2180", 0, None],
]


def get_random_api_key():
  selected_key_index = -1
  while selected_key_index == -1:
    random_index = random.randint(0, len(API_KEYS)-1)

    print(API_KEYS[random_index][2])
    if API_KEYS[random_index][1] == 9:
      last_request_timestamp = API_KEYS[random_index][2]
      print(last_request_timestamp)
      if last_request_timestamp != None:
        print(datetime.datetime.now().timestamp() - last_request_timestamp)
        if datetime.datetime.now().timestamp() - last_request_timestamp:
          API_KEYS[random_index][2] = None 
        else:
          # Key still waiting to be refreshed
          continue
    
    selected_key_index = random_index
    break
  return API_KEYS[selected_key_index], selected_key_index


for i in range(1000):
  key, key_index = get_random_api_key()
  API_KEYS[key_index][2] = datetime.datetime.now().timestamp()
  API_KEYS[key_index][1] += 1
  if key[1] == 10:
    print("Full key returned.: ", i)
    break

# Control structure loop variables
# is_reached_end = False
# count = 0
# today = datetime.datetime.now()
# endpoints = list()
# data = list()
# loaded_requests = 0
# total_count = 0
# TOTAL_DATA_REQUIRED = 30_000

# # Gets the matches from the football API.
# def get_matches(url, api_key):
#   response = requests.get(url,
#                     headers={'X-Unfold-Lineups': "true",
#                              'X-Unfold-Goals': "true",
#                              'X-Auth-Token': api_key})
#   if response.status_code == 200:
#     return response.json()["matches"]
#   else:
#     return [], 


# while is_reached_end == False:
#   try:
#     timedelta = datetime.timedelta(days=10)
#     past_ten_days = today - timedelta
#     endpoint = f"https://api.football-data.org/v4/matches?competitions=PL&dateTo={today.strftime('%Y-%m-%d')}&dateFrom={past_ten_days.strftime('%Y-%m-%d')}"

#     API_KEY = get_random_api_key()[0]
#     matches = get_matches(endpoint, API_KEY[0])
#     print(f"Loaded: {len(matches)} matches. Date: {today} - {past_ten_days}.")

#     if matches:
#         for match_ in matches:
#             data.append([
#                 match_["id"],
#                 match_["utcDate"], # date
#                 match_["status"], # status
#                 match_["competition"]["name"], # league_name
#                 match_["competition"]["type"], # league_type
#                 match_["stage"], # stage
#                 match_["homeTeam"]["shortName"], # home_name
#                 match_["homeTeam"]["id"], # home_id
#                 match_["awayTeam"]["shortName"], # away_name
#                 match_["awayTeam"]["id"], # away_id
#                 match_["score"]["halfTime"]["home"], # score_home_ht
#                 match_["score"]["halfTime"]["away"], # score_away_ht
#                 match_["score"]["fullTime"]["home"], # score_home_ft
#                 match_["score"]["fullTime"]["away"], # score_away_ft
#             ])
            
#             total_count += 1 # match request = +9, total = 10, then loop resets back to 0.
#             print(f'Progressive percentage: {total_count} ({round((total_count/TOTAL_DATA_REQUIRED)*100, 2)}%)')

#     # End while loop when required sample size has been reached.
#     if (API_KEY[1] == 10):
#         is_reached_end = True
#         break
#     else:
#         # Else keep the while loop running.
#         today = past_ten_days
#   except:
#     print(traceback.format_exc())

#     # Incase something goes wrong with the above script, save current progress.
#     df = pd.DataFrame(data, columns=["id", "date", "status", "league_name", "league_type", "stage", "home_team", "home_team_id", "away_team", "away_team_id", "score_home_ht", "score_away_ht", "score_home_ft", "score_away_ft"])
#     df.to_csv(f"../relative_datasets/raw/premier_leage_{total_count}.csv", index=False)
        
#     # Await the next 60 seconds to be allowed to request more data, incase limit has been reached.
#     time.sleep(60)
#     continue

# df = pd.DataFrame(data, columns=["id", "date", "status", "league_name", "league_type", "stage", "home_team", "home_team_id", "away_team", "away_team_id", "score_home_ht", "score_away_ht", "score_home_ft", "score_away_ft"])
# df.to_csv(f"../relative_datasets/raw/premier_leage.csv", index=False)