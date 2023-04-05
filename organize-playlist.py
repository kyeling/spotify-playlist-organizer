import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
from util import *

#  initial funtion to access spotify account
raise NotImplementedError('Please fill out authentication credentials.')
def authenticate():
    with open('access/client_id.txt', 'r') as f:
        id = f.read().rstrip()
    
    with open('access/client_secret.txt', 'r') as f:
        secret = f.read().rstrip()

    creds = {
        'client_id': id,
        'client_secret': secret,
        'redirect_uri': 'https://api.spotify.com/v1',
        'scope': 'user-library-read playlist-modify-public'
    }
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(**creds))
    return sp

# extract id from user info
def get_user_id():
    return sp.current_user()['id']

# get unique playlist id from playlist name
def get_playlist_id(name):
    # returns a list of all public playlists added to current user's profile
    playlists = sp.current_user_playlists()['items']

    # returns first found occurrence for multiple playlists of the same name
    playlist_id = list(filter(lambda p: p['name']==name, playlists))[0]['id']
    return playlist_id 

# retrieve all items in a given playlist, 100 items at a time
# src: https://stackoverflow.com/questions/39086287/spotipy-how-to-read-more-than-100-tracks-from-a-playlist
def get_playlist_items(name):
    playlist_id = get_playlist_id(name)
    results = sp.playlist_items(playlist_id)
    items = results['items']
    while results['next']:
        results = sp.next(results)
        items.extend(results['items'])
    return items

# sort tracks by artist alphanumerical order, then album and order in album
def sort_tracks(name, sort_func):
    songs = get_playlist_items(name)
    tracks = list(map(exTRACKt, songs))
    tracks.sort(key=lambda t: sort_func(t))

    ids = list(map(lambda t: t['id'], tracks))  
    return ids

# add tracks by id (100 at a time) to a playlist
def add_tracks(name, track_ids):
    playlist_id = get_playlist_id(name)
    for i in range(0, len(track_ids), 100):
        sp.user_playlist_add_tracks(user, playlist_id, track_ids[i:i+100])

# create new playlist and add tracks 
def create_playlist(new_name):
    sp.user_playlist_create(user, new_name)
    add_tracks(new_name, track_ids)

# clear all tracks (100 at a time) in a playlist without deleting it
def clear_playlist(name, track_ids):
    playlist_id = get_playlist_id(name)
    for i in range(0, len(track_ids), 100):
        sp.user_playlist_remove_all_occurrences_of_tracks(user, playlist_id, track_ids[i:i+100])

# clears a playlist and adds the tracks back in sorted order
def sort_playlist(name, track_ids):
    clear_playlist(name, track_ids)
    add_tracks(name, track_ids)

if __name__ == '__main__':
    # parse cmd line args
    name = sys.argv[1] # make sure playlist is added to profile
    sortby = sortby_artist # select a sorting key from util.py

    # setup
    sp = authenticate()
    user = get_user_id()
    
    # create/modify playlist with sorted order
    track_ids = sort_tracks(name, sortby)
    with open(f'{name}-track-ids.txt', 'w') as f:
        f.write('\n'.join(track_ids))

    sort_playlist(name, track_ids)
