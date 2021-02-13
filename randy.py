import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os.path
import time

redirectUri = "https://example.com/callback"
fileName = "secrets.json"
tracksToPlay = 4

if os.path.isfile(fileName):
    with open(fileName) as openedFile:
        data = json.load(openedFile)
        clientId = data['name']
        clientSecret = data['secret']
else:
    clientId = input("enter client id: ")
    clientSecret = input("enter user secret: ")
    secrets = {"name":clientId, "secret":clientSecret}
    with open(fileName, "w") as json_file:
        json.dump(secrets, json_file)

#print(clientId)
#print(clientSecret)
#print(redirectUri)

scope = "user-library-read streaming user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=clientId, client_secret=clientSecret, redirect_uri=redirectUri))

playlists = sp.current_user_playlists()
print(type(playlists))
print("Available Playlists:")

for playlist in playlists['items']:
    print(playlist['name'])

playlistName = input("What playlist do you wanna play? ")
print("playing " + playlistName)

for playlist in playlists['items']:
    if playlist['name'] == playlistName:
        playlistId = playlist['id']
        playlistUri = playlist['uri']
        break
# TODO: errorhandling if playlist not found

sp.start_playback(context_uri=playlistUri)
sp.shuffle(True)

playbackDict = dict()
# continuously read
# break with Ctr+C
for i in range(tracksToPlay):
    time.sleep(5)
    currentPlayback = sp.current_playback()
    trackIdAndName = currentPlayback['item']['id'] + " " + currentPlayback['item']['name']
    if trackIdAndName in playbackDict:
        playbackDict[trackIdAndName] += 1
    else:
        playbackDict[trackIdAndName] = 1
    print(trackIdAndName)
    sp.next_track()

print(playbackDict)
