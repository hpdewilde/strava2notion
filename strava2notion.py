# Imports
import json
import os
import requests
import time

# Strava credentials
client_id = 'xxx'
client_secret = 'xxx'
redirect_uri = 'http://localhost/'

# Notion credentials
NOTION_TOKEN = "xxx"
DATABASE_ID = "xxx"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# STRAVA FUNCTIONS

# Request OAuth access token
def request_token(client_id, client_secret, code):
    response = requests.post(url='https://www.strava.com/oauth/token',
                             data={'client_id': client_id,
                                   'client_secret': client_secret,
                                   'code': code,
                                   'grant_type': 'authorization_code'})
    return response

# Refresh OAuth access token in case it expired
def refresh_token(client_id, client_secret, refresh_token):
    response = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                             data={'client_id': client_id,
                                   'client_secret': client_secret,
                                   'grant_type': 'refresh_token',
                                   'refresh_token': refresh_token})
    return response

# Write OAuth access token to JSON file
def write_token(token):
    with open('strava_token.json', 'w') as outfile:
        json.dump(token, outfile)

# Get OAuth access token from JSON file
def get_token():
    with open('strava_token.json', 'r') as token:
        data = json.load(token)
    return data

# ONE TIME STRAVA AUTHORIZATION (ONLY FIRST TIME OF RUNNING SCRIPT)

if not os.path.exists('./strava_token.json'):
    request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_uri}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

    print('Click here:', request_url)
    print('Please authorize the app and copy&paste below the generated code!')
    print('P.S: you can find the code in the URL')
    code = input('Insert the code from the url: ')
    
    token = request_token(client_id, client_secret, code)

    # Save JSON response as a variable
    strava_token = token.json()
    # Save tokens to file
    write_token(strava_token)

data = get_token()

# Refresh OAuth access token in case it expired
if data['expires_at'] < time.time():
    print('Refreshing token!')
    new_token = refresh_token(client_id, client_secret, data['refresh_token'])
    strava_token = new_token.json()
    # Update the file
    write_token(strava_token)

data = get_token()

access_token = data['access_token']

# Retrieve activities from Strava
activities_url = f"https://www.strava.com/api/v3/athlete/activities?" \
          f"access_token={access_token}"

response = requests.get(activities_url)

# NOTION FUNCTIONS

# Add new entry to Notion database
def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages/"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)

    if res.status_code == 200:
        print("Successfully added Strava activity to Notion.")
    else:
        print("An error occurred.")

    return res

# Get information from entries in Notion database
def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages
    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    results = data["results"]
    
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

# Create list of activity dates that are already in the Notion database (will be used later to prevent duplicate entries)
pages = get_pages()
activity_dates = [page['properties']['Date']['date']['start'][:16] for page in pages]

# Iterate over Strava activities
for activity in response.json():
    # Check if activity is already in Notion database. If so, all following activities are also in the Notion database already
    if activity['start_date'][:16] in activity_dates:
        print("All activities from Strava have been uploaded to Notion.")
        break

    # Add information from Strava activity to new entry in Notion database
    name = activity['name']
    date = activity['start_date']
    distance = activity['distance']
    avg_speed = activity['average_speed']
    max_speed = activity['max_speed']
    moving_time = round(activity['moving_time'] / 60, 2)

    data = {
        "Name": {"title": [{"text": {"content": name}}]},
        "Date": {"date": {"start": date, "end": None}},
        "Distance (m)": {"number": distance},
        "Average speed (m/s)": {"number": avg_speed},
        "Max speed (m/s)": {"number": max_speed},
        "Moving time (minutes)": {"number": moving_time}
    }

    create_page(data)