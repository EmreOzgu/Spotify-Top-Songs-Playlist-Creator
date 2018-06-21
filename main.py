import sys
import spotipy
import spotipy.util as util
import requests
from datetime import datetime

#Searches 250 songs for the given keyword and returns a list of all of the tracks.
def search(key, sp):

    try:
        results1 = sp.search(q=key, limit=50, offset=0, type='track')
        results2 = sp.search(q=key, limit=50, offset=50, type='track')
        results3 = sp.search(q=key, limit=50, offset=100, type='track')
        results4 = sp.search(q=key, limit=50, offset=150, type='track')
        results5 = sp.search(q=key, limit=50, offset=200, type='track')
    except requests.exceptions.RequestException:
        print ("Too many requests. Try again in a few moments.")
        sys.exit(1)

    result = results1['tracks']['items'] + results2['tracks']['items'] + results3['tracks']['items'] + results4['tracks']['items'] + results5['tracks']['items']
    
    return result

#Cleans a string up from non-letters.
def cleanup(s):
    result = ""
    for char in s:
        if char.isalpha():
            result = result + char
    return result

#Checks if a track is the same as another track already in a list of tracks.
def is_copy(track, tracks):
    name1 = cleanup(track['name'])
    for t in tracks:
        name2 = cleanup(t['name'])
        if name1 in name2 or name2 in name1:
            return True
    return False

#Creates the desired playlist.
def create_playlist(sp, key, items, allow_recent):
    max = 0

    #Finds the most popular track.
    for i in items:
        if i['popularity'] > max:
            max = i['popularity']
            top_track = i

    playlist_name = key + " - Python"

    playlist = sp.user_playlist_create(username, playlist_name)

    threshold = max - (max / 4)

    #List of track IDs for the playlist
    tracks = []

    #List of track objects that are going to added to the playlist.
    added = []

    #Adds tracks that of the top 25th percentile to the playlist.
    for i in items:
        if i['popularity'] > threshold and not is_copy(i, added):  
            if not allow_recent and is_recent(i):
                continue
            tracks.append(i['id'])
            added.append(i)
            
    sp.user_playlist_add_tracks(username, playlist['id'], tracks)

#Returns true if a track is released within the last 2 months.
def is_recent(track):

    #If release date precision is more precise than a year, continue checking.
    if track['album']['release_date_precision'] != 'year':
        release_date = track['album']['release_date']
        i = release_date.index('-')
        year = int(release_date[:i])
        release_date = release_date[i + 1:i + 3]
        month = int(release_date)
        
        return datetime.now().year == year and datetime.now().month - month  <= 2

    else:
        print("old")
        return False


scope = 'playlist-modify-public'

username = input('Your Spotify username: ')  
    
token = util.prompt_for_user_token(username, scope)

key = input('Enter playlist theme: ')

if input('Would you like to ignore recent releases? (Recent releases can have higher \'popularity\' and may appear more in the playlist.) (y/n) ? ') == 'y':
    allow_recent = False
else:
    allow_recent = True

print('Generating playlist...')

#Does an exact search on Spotify, using quotation marks.
key = '"' + key + '"'

sp = spotipy.Spotify(auth=token)

items = search(key, sp)

create_playlist(sp, key, items, allow_recent)

input('Success! Press ENTER to exit.')
