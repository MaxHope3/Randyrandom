import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os.path
import time

redirectUri = "https://example.com/callback"    # Url where the auth will redirect to, doesn't really matter
fileName = "secrets.json"                       # name of file where we store the clientId and the clientSecret for the API
tracksToPlay = 30                               # number of tracks to play each run
runsToRun = 100                                 # number of runs

# Either load clientsecret from file, or (if not existent) ask user for input
if os.path.isfile(fileName):                # check if file exists
    with open(fileName) as openedFile:      # open file as 'openedFile'
        data = json.load(openedFile)        # load as dict (json)
        clientId = data['name']             # get clientId fron dict
        clientSecret = data['secret']       # get clientData from dict
else:
    clientId = input("enter client id: ")               # get userinput for clientId
    clientSecret = input("enter user secret: ")         # get userinput for clientSecret
    secrets = {"name":clientId, "secret":clientSecret}  # create dictionary with values
    with open(fileName, "w") as jsonFile:               # open file as json_file
        json.dump(secrets, jsonFile)                    # save dictionary in file

# permissions the app needs
# user-library-read:        for getting what playlists the user has
# streaming:                for starting playback (some other playback needs to be started already manually)
# user-read-playback-state: for reading what song is currently playing
scope = "user-library-read streaming user-read-playback-state" 

# create spotify object
# will open browser window for authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=clientId, client_secret=clientSecret, redirect_uri=redirectUri))

playlists = sp.current_user_playlists() # get all playlists

# print all available playlists
print("Available Playlists:")
for playlist in playlists['items']:
    print(playlist['name'])

# get userinput on what playlist to play
playlistName = input("What playlist do you wanna play? ")
print("playing " + playlistName)

for playlist in playlists['items']:         # iterate over all available playlists
    if playlist['name'] == playlistName:    # check if name is equal to userInput
        playlistUri = playlist['uri']       # save URI of palylist
        break                               # exit loop
# TODO: errorhandling if playlist not found

playbackDict = dict()       # create dictionary for results

for run in range(runsToRun):    # run 'runsToRun' times
    sp.start_playback(context_uri=playlistUri)  # start playback of selected playlist
    sp.shuffle(True)                            # set shuffle to true

    # continuously read what song plays
    for i in range(tracksToPlay):   # run 'tracksToPlay' times
        time.sleep(5)               # delay at first, so the information is refreshed for sure
        currentPlayback = sp.current_playback()     # get current playback
        trackIdAndName = currentPlayback['item']['id'] + " " + currentPlayback['item']['name']      # save ID and Trackname in string to create unique key. (e.g. 'trackID trackName')
        if trackIdAndName in playbackDict:          # check if track is already in dict
            playbackDict[trackIdAndName] += 1       # increment counter
        else:
            playbackDict[trackIdAndName] = 1        # add track to dict
        print(trackIdAndName)                       # output
        sp.next_track()                             # skip to next track

# output and print result dictionary
print(playbackDict)
with open("results.json", "w") as results:
    json.dump(playbackDict, results)
