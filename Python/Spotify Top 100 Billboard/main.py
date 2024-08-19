import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

# Spotify Account Info
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:1234",
                                               scope=scope))

# Create Spotify Playlist
def create_playlist(date):
    personal_id = sp.current_user()['id']
    playlist = (sp.user_playlist_create(user=personal_id, name=f"Billboard Top 100 {date}", public=False))
    print(f"Playlist: Billboard {date} created successfully")
    return playlist["id"]


# Add songs from Billboard to Playlist
def add_songs(playlist_id, track_uri):
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uri)

# Find the tracks from the Billboard Top 100
def search_artist_track(track_name):
    try:
        query = f"track:{track_name} year:2000"
        results = sp.search(q=query, type="track", limit=10)
        tracks = str(results["tracks"]["items"][0]["uri"])
        return tracks.split(':')[-1]
    except IndexError:
        pass

# Use Beautiful Soup to analyze the Billboard Top 100 and put them in a list
def make_soup(date):
    URL = f"https://www.billboard.com/charts/hot-100/{date}/"

    response = requests.get(URL)
    billboard_web = response.text

    soup = BeautifulSoup(billboard_web, "html.parser")

    top_100 = soup.find_all(name="h3", id="title-of-a-story")

    all_songs = [song.getText().strip() for song in top_100]

    clean_songs = all_songs[6::4]

    song_uri = []

    for song in clean_songs:
        track = (search_artist_track(song))
        if track is not None:
            song_uri.append(track)

    return song_uri


date_playlist = str(input("What time would you like to go to? (YYYY-MM-DD): "))

playlist_id = create_playlist(date_playlist)

songs = make_soup(date_playlist)

print(len(songs))

add_songs(playlist_id, songs)

