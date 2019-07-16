
import json
import requests
import base64
import urllib.parse


# Client Keys
CLIENT_ID = "2c8e46b5fcb24783b6be3c10b6f512a5"
CLIENT_SECRET = "d27db5eae5b64213b64a0c929efbb07b"

#Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

#Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
# CLIENT_SIDE_URL = "url 'spotify_auth'"
PORT = 8000
REDIRECT_URI = "{}:{}/PittsTime/spotify/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-library-read user-read-email"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

#Authorization of application with spotify
def app_Authorization():
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        # "state": STATE,
        # "show_dialog": SHOW_DIALOG_str,
        "client_id": CLIENT_ID
    }
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return auth_url

#User allows us to acces there spotify
def user_Authorization(auth_token):
    # auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = (base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode("utf-8"))).decode('utf-8')
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    return authorization_header

#Gathering of profile information
def Profile_Data(header):
    # Get user profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=header)
    profile_data = json.loads(profile_response.text)
    return profile_data

#Gathering of playlist information
def Playlist_Data(header,profile):
    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=header)
    playlist_data = json.loads(playlists_response.text)
    return playlist_data

#Gathering of album information
def Album_Data(header,profile,limit,offset):
    # Get user albums data
    artist_api_endpoint = ("{}/albums?limit=" + str(limit) + "&offset=" + str(offset)).format(profile["href"])
    artist_response = requests.get(artist_api_endpoint, headers=header)
    artist_data = json.loads(artist_response.text)
    return artist_data

def Track_Data(header,q):
    #Get track data
    params = (
        ('q', q),
        ('type', 'track'),
        ('limit', '5'),
        ('offset', '0'),
    )
    track_api_endpoint = "{}/search".format(SPOTIFY_API_URL)
    track_response = requests.get(track_api_endpoint, headers=header, params=params)
    track_data = json.loads(track_response.text)
    uris = []
    for track in track_data.get('tracks').get('items'):
        uris.append(track.get('uri'))

    # uri = track_data.get('tracks').get('items')[0].get('uri')
    return uris

def Button_src(uri):
    code = str(uri).replace("spotify:track:", "")
    iframe = "https://open.spotify.com/embed/track/{}".format(code)
    return iframe
