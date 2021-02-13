import spotipy
from spotipy.oauth2 import SpotifyOAuth

clientId = input("enter client id: ")
clientSecret = input("enter user secret: ")
redirectUri = "https://example.com/callback"

#print(clientId)
#print(clientSecret)
#print(redirectUri)

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=clientId, client_secret=clientSecret, redirect_uri=redirectUri))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])