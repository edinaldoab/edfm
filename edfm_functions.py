# import datetime
import os
import time

import pandas as pd
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SPOTIPY_CLIENT_ID = 'seu_client_id'
SPOTIPY_CLIENT_SECRET = 'seu_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/'
SCOPE = 'user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))


def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids


def get_genres(artist_name):
    result = sp.search(artist_name)
    track_result = result['tracks']['items'][0]
    artist_result = sp.artist(
        track_result['artists'][0]['external_urls']['spotify'])

    return artist_result['genres']


def get_first_genre(genre_list):
    length = len(genre_list)

    if length != 0:
        first_genre = genre_list[0]
    else:
        first_genre = 'NA'

    return first_genre


def get_track_info(id):
    meta = sp.track(id)
    features = sp.audio_features(id)
    artist_features = sp.artist(meta['album']['artists'][0]['id'])

    track_name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_year = meta['album']['release_date'][0:4]
    track_data_concat = track_name + '\n' + \
        artist + '\n' + album + '\n' + release_year
    first_genre_assigned = get_first_genre(get_genres(artist))
    spotify_url = meta['external_urls']['spotify']
    artist_image = artist_features['images'][0]['url']
    album_cover = meta['album']['images'][0]['url']
    danceability = features[0]['danceability']
    valence = features[0]['valence']

    track_info = [track_name,
                  album,
                  artist,
                  release_year,
                  track_data_concat,
                  first_genre_assigned,
                  valence,
                  danceability,
                  spotify_url,
                  artist_image,
                  album_cover]

    return track_info


def insert_to_csv(track_ids, time_period):

    tracks = []
    for i in range(len(track_ids)):
        position = i+1
        time.sleep(.5)
        track = get_track_info(track_ids[i])
        track.append(position)
        track.append(time_period)
        tracks.append(track)

    df = pd.DataFrame(
        tracks, columns=['track_name',
                         'album',
                         'artist',
                         'release_year',
                         'track_data_concat',
                         'first_genre_assigned',
                         'valence',
                         'danceability',
                         'spotify_url',
                         'artist_image',
                         'album_cover',
                         'position',
                         'period'])

    # current_date = datetime.date.today().strftime('%Y-%m-%d')

    df.to_csv(f'{time_period}.csv')

    print(f'"{time_period}" data downloaded!\n')
    return tracks


def combine_csvs():
    df = pd.DataFrame()

    for file in os.listdir(os.getcwd()):
        if file.endswith('.csv'):
            df = df.append(pd.read_csv(file))

    df.to_csv('merged_data.csv', index=False)


def delete_current_csvs():
    i = 0
    for file in os.listdir(os.getcwd()):
        if file.endswith('.csv'):
            os.remove(file)
            i = i + 1

    print(f'\n{i} csvs have been removed.\n')
