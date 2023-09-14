# strava2notion
This script loads all your Strava activities into a Notion database. Please follow the steps below in order to successfully run the script.

## Preparation

### Strava
1. Go to https://www.developers.strava.com and click on 'Create & Magage Your App'.
2. Create your app. It does not matter what information you fill in, but make sure your Authorization Callback Domain is set to 'localhost'.
3. After creating the app, you should be able to see your Client ID and Client Secret. Copy and paste these codes into the strava2notion.py file.

### Notion
1. Go to https://www.notion.so/my-integrations and click on 'Create new integration'.
2. Select the 'Associated workspace' where your Notion database will be located and give your integration a fitting name (e.g. 'Strava').
3. View your newly created integration and copy and paste the 'Internal Integration Secret' code into the strava2notion.py file.
4. Create a new database in the Notion workspace that you selected for your integration earlier.
5. Click the three dots in the top right corner, click 'Add connections' and select the integration that you just created.
6. In the URL of your Notion database, find the database ID. It is found between the '/' after your username and the '?' that is also in the URL.
7. Copy and paste the database ID into the strava2notion.py file.
8. In your Notion database, keep the 'Name' column, delete the 'Tags' column, and create the following columns:
    * 'Date' (using the date property)
    * 'Distance (m)' (using the number property)
    * 'Average speed (m/s)' (using the number property)
    * 'Max speed (m/s)' (using the number property)
    * 'Moving time (minutes)' (using the number property)
  
## Running the script
Now you're ready to run the script! Run it in your preferred Python environment and follow the steps the script gives you. The first time running the script, you will need to authorize Strava (the script provides the steps on how to do so), but you won't have to authorize again the next time you run the script. 

If all goes well, the script will start printing "Successfully added Strava activity to Notion." for every Strava activity that was added to your Notion database. Check your Notion database to see if the activities have indeed appeared there. If all activities have been added to your Notion database already (if you run the script multiple times in a short amount of time for example), the script will let you know by printing "All activities from Strava have been uploaded to Notion."
