from bs4 import BeautifulSoup
import requests
from spotify_playlist import SpotifyPlaylist

spotify_playlist = SpotifyPlaylist()

PLAYLIST_NAME = ""


def get_top_100():
    """
    Use BeautifulSoup to scrape the data from the billboard
    """
    global PLAYLIST_NAME
    year = input("Which year do you want to check? Type the date in this format YYYY-MM-DD: ")
    billboard_url = f"https://www.billboard.com/charts/hot-100/{year}"
    response = requests.get(billboard_url)
    top_100_page = response.text
    soup = BeautifulSoup(top_100_page, "html.parser")
    top_100_songs = []
    for entry in soup.find_all(attrs={"class": "o-chart-results-list-row-container"}):
        top_100_songs.append({
            "title": entry.h3.getText(strip=True),
            "artist": entry.h3.findNext("span").getText(strip=True)
        })

    PLAYLIST_NAME = f"{year} Billboard 100"
    return top_100_songs


all_billboard_playlists = spotify_playlist.existing_playlist()
if len(all_billboard_playlists) == 0:
    top_100_songs = get_top_100()
    spotify_playlist.create_playlist(PLAYLIST_NAME)
    spotify_playlist.add_to_playlist(top_100_songs)
else:
    print("Your current billboard playlists:")
    for playlist in all_billboard_playlists:
        print(playlist)
    top_100_songs = get_top_100()
    spotify_playlist.create_playlist(PLAYLIST_NAME)
    spotify_playlist.add_to_playlist(top_100_songs)
