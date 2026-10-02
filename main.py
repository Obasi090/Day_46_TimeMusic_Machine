from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

# STEP 1: Get the user's date
def get_date():
    while True:
        input_music_date = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")
        split_music_date = input_music_date.split("-")

        # 1. Check if it has exactly 3 parts (Year, Month, Day)
        if len(split_music_date) != 3:
            print("Invalid date format. You must use the YYYY-MM-DD format with two dashes.")
            continue

        # 2. Optional: Ensure all parts are numbers (e.g., prevents "YYYY-MM-DD")
        if not all(part.isdigit() for part in split_music_date):
            print("Invalid characters. The year, month, and day must be numbers.")
            continue
        try:
            music_travel_date = datetime.strptime(input_music_date, "%Y-%m-%d")
        except ValueError:
            print("That is not a valid date.")
        else:
            return music_travel_date.year, music_travel_date.strftime("%Y-%m-%d")

# STEP 2: Get Billboard HTML
def get_bakeboard_html(music_travel_date):
    base_url = os.getenv("BILLBOARD_URL")
    url = f"{base_url}/{music_travel_date}/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"Could not retrieve the webpage: {error}")
        return None
    else:
        return response.text

# STEP 3: Extract songs
def get_song_names(html):
    soup = BeautifulSoup(html, "html.parser")

    #song_number = soup.find_all("span", class_ = "chart-entry__rank-number")
    song_name = soup.find_all("h3", class_ = "chart-entry__title")
    song_artist = soup.find_all("span", class_ = "chart-entry__artist")

    #music_numbers = [numbers.getText() for numbers in song_number]
    songs = [title.getText() for title in song_name]
    artists = [artist.getText() for artist in song_artist]

    song = list(zip(songs, artists))
    return song

# STEP 4: Authenticate Spotify
def get_spotify_user_id():
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope=os.getenv("SCOPE"),
        requests_timeout=10,
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_profile = sp.current_user()

    user_id = user_profile["id"]

    return sp, user_id

# STEP 5: Normalize song titles
def normalize_title(title):
    title = title.lower()

    title = title.replace("’", "'")

    if " (with " in title:
        title = title.split(" (with ")[0]

    if " (feat. " in title:
        title = title.split(" (feat. ")[0]

    if " (feat " in title:
        title = title.split(" (feat ")[0]

    return title.strip()

# STEP 6: Normalize artists
def get_requested_artists(artist):
    artist = artist.lower()

    artist = artist.replace(" featuring ", "&")
    artist = artist.replace(" feat. ", "&")
    artist = artist.replace(" feat ", "&")
    artist = artist.replace(" with ", "&")
    artist = artist.replace(",", "&")
    artist = artist.replace(":", "&")

    return [
        name.strip()
        for name in artist.split("&")
        if name.strip()
    ]

# STEP 7: Search Spotify
def find_spotify_track(sp, song, artist, song_year):
    query = f"track: {song} artist: {artist} year: {song_year}"

    try:
        results = sp.search(q=query, type="track", limit=5)

        tracks = results["tracks"]["items"]

        found_track = None

        requested_artists = get_requested_artists(artist)
        requested_title = normalize_title(song)

        for track in tracks:

            spotify_artists = [
                artist["name"].lower()
                for artist in track["artists"]
            ]

            title_matches = normalize_title(track["name"]) == requested_title

            artist_matches = all(
                requested_artist in spotify_artists
                for requested_artist in requested_artists
            )

            if title_matches and artist_matches:
                found_track = track
                break

        if found_track:
            print(
                f"Found: {found_track['name']} - "
                f"{', '.join(a['name'] for a in found_track['artists'])}"
            )
        else:
            print(f"No exact match found for {song}")

        return found_track

    except Exception as error:
        print(f"Error searching for {song}: {error}")
        return None

# STEP 8: Create playlist
def create_playlist(sp, song_uris):
    playlist_name = input("Give your playlist a name: ")

    playlist = sp.current_user_playlist_create(name = playlist_name,
                                               public=False,
                                               description="A python project of scraping 100 songs")

    playlist_id = playlist["id"]
    print(f"Successfully created playlist: {playlist_name} with ID: {playlist_id}")

    if song_uris:
        sp.playlist_add_items(
            playlist_id=playlist_id,
            items=song_uris
        )
        print(f"Added {len(song_uris)} songs to your new playlist!")
    else:
        print("No songs were found to add to the playlist.")


song_year, chart_date = get_date()
bakeboard_html = get_bakeboard_html(chart_date)
if bakeboard_html is None:
    print("Could not fetch chart data. Exiting.")
    exit()
songs = get_song_names(bakeboard_html)
sp, user_id = get_spotify_user_id()
song_uris = []
for song, artist in songs:
    print(f"Searching: {song} by {artist}")

    found_track = find_spotify_track(
        sp,
        song,
        artist,
        song_year
    )
    if found_track:
        song_uris.append(found_track["uri"])
create_playlist(sp, song_uris)
