import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyPlaylist:
    USER = os.getenv('USER_ID')

    def __init__(self):
        self.playlist_id = ""
        self.sp = None
        self.authenticate("")

    def create_playlist(self, playlist_name):
        """Creates a new billboard playlist"""
        scope = "playlist-modify-private"
        self.authenticate(scope)
        new_playlist = self.sp.user_playlist_create(name=playlist_name,
                                                    description="Top 100 billboard songs", public=False,
                                                    user=self.USER)
        self.playlist_id = new_playlist["id"]

    def existing_playlist(self):
        """Collects all the existing billboard playlist and returns a list of playlist names"""
        scope = "playlist-read-private"
        self.authenticate(scope)
        result = self.sp.user_playlists(user=self.USER, limit=10)
        playlist_names = [item['name'] for item in result['items'] if
                          item['owner']['id'] == self.USER]
        return playlist_names

    def add_to_playlist(self, top_100):
        """top_100 contains the top 100 songs from the billboard based on specific date.
        Search each tract on Spotify and add it to the playlist.
        """
        song_uris = []
        for entry in top_100:
            result = self.sp.search(q=f"track: {entry["title"]} artist: {entry["artist"]}",
                                    type="track", limit=1, market="US")
            try:
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
            except IndexError:
                print("The song does not exist in Spotify.")

        self.sp.playlist_add_items(self.playlist_id, song_uris)

    def authenticate(self, scope):
        """Spotify will provide the client_id and client_secret after creating the app in the https://developer.spotify.com/dashboard"""
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=os.getenv("SPOTI_ID"),
                                                            client_secret=os.getenv("SPOTI_SECRET"),
                                                            redirect_uri="https://example.com/"))
