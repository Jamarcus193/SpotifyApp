from SpotifyUser import User
import Playlist
import os

user = User()
user.start()

playlistName = user.choosePlaylist()

