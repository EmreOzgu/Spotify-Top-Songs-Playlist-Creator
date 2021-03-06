import sys
import spotipy
import spotipy.util as util
import requests
from datetime import datetime

def search(key, sp):
    ''' Searches 250 songs for the given keyword and returns a list of all of the tracks. '''
    result = []
    try:
        for i in range(5):
            result += sp.search(q=key, limit=50, offset=i*50, type='track')['tracks']['items']
    except requests.exceptions.RequestException:
        print ("Too many requests. Try again in a few moments.")
        sys.exit(1)

    return result

def cleanup(s):
    ''' Cleans a string up from non-letters. '''
    result = ""
    for char in s:
        if char.isalpha():
            result = result + char
    return result

def is_copy(track, tracks):
    ''' Checks if a track is the same as another track already in a list of tracks. '''
    name1 = cleanup(track['name'])
    
    for t in tracks:
        name2 = cleanup(t['name'])
        if name1 in name2 or name2 in name1:
            return True
    return False

def create_playlist(sp, key, items, allow_recent):
    ''' Creates the desired playlist. '''
    max = 0

    #Finds the most popular track.
    for i in items:
        if i['popularity'] > max:
            max = i['popularity']
            top_track = i

    playlist_name = key + " - Python"

    playlist = sp.user_playlist_create(username, playlist_name)

    threshold = max - (max / 3.6)

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

def is_recent(track):
    ''' Returns true if a track is released within the last 2 months. '''

    #If release date precision is more precise than a year, continue checking.
    if track['album']['release_date_precision'] != 'year':
        release_date = track['album']['release_date']
        i = release_date.index('-')
        year = int(release_date[:i])
        release_date = release_date[i + 1:i + 3]
        month = int(release_date)
        
        return datetime.now().year == year and datetime.now().month - month  <= 2

    else:
        return False

def process_playlists(username, sp, playlists):
    ''' Gets a string of playlist names, and returns the playlist IDs as a list. '''
    result = []
    names = []
    while playlists.find(',') != -1:
        i = playlists.find(',')
        names.append(playlists[:i])
        playlists = playlists[i + 2:]
    all_playlists = sp.user_playlists(username)
    for n in names:
        for p in all_playlists['items']:
            if p['name'] == n and p['public']:
                result.append(p['id'])
                break
    return result




# START OF MAIN

scope = 'playlist-modify-public'

username = input('Your Spotify username: ')  
    
token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)

allow_recent = True

print("Menu:")
print("s - Make a top songs playlist around a keyword theme (Star Wars, World of Warcraft, etc.) or artist")
print("p - Make a top songs playlist from your given public playlists")

pref = ''

while pref != 's' and pref != 'p':
    pref = input("Your Choice? ")

items = []

if pref == 's':
    key = input('Enter playlist theme: ')
    key = '"' + key + '"'

    if input('Would you like to ignore recent releases? (Recent releases can have higher \'popularity\' and may appear more in the playlist.) (y/n) ? ') == 'y':
        allow_recent = False

    print("Creating...")
    sys.stdout.flush()

    items = search(key, sp)

elif pref == 'p':
    playlists = process_playlists(username, sp, input('Enter the names of your playlists you would like to choose songs from (seperated by a comma and a space): '))
    playlist_items = []
    for p in playlists:
        playlist_items += sp.user_playlist_tracks(username, p)['items']

    for p in playlist_items:
        items.append(p['track'])
    key = input('Enter Name of New Playlist: ')
    
create_playlist(sp, key, items, allow_recent)

input('Success! Press ENTER to exit.')
