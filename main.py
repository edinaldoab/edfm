import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from edfm_functions import (combine_csvs, delete_current_csvs, get_track_ids,
                            insert_to_csv)

load_dotenv()
SPOTIPY_CLIENT_ID = 'seu_client_id'
SPOTIPY_CLIENT_SECRET = 'seu_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/'
SCOPE = 'user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

delete_current_csvs()

time_ranges = ['short_term', 'medium_term', 'long_term']

for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(
        limit=50, offset=0, time_range=time_period)
    track_ids = get_track_ids(top_tracks)
    insert_to_csv(track_ids, time_period)

combine_csvs()
