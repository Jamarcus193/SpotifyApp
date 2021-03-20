import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

def getIndex(name, lst):
    return lst.index(name)

#Create the playlist
def createPlaylist(username, spotifyObject):
    playlistName = input('Enter a playlist name: ')
    playlist_descr = input('Enter a playlist description: ')

    spotifyObject.user_playlist_create(user=username, name=playlistName,public=True,description=playlist_descr)

    user_input = input('Enter a song: ')
    songList = [] #list of uris pulled from a playlist

    while user_input != 'quit':
        result = spotifyObject.search(q=user_input)
        #print(json.dumps(result,sort_keys=5,indent=4))
        #index = getSongIndex(result, user_input, artist)    
        songList.append(result['tracks']['items'][0]['uri'])
        user_input = input('Enter the song:')

    #find the playlist
    prePlaylist = spotifyObject.user_playlists(user=username)
    for i in range(len(prePlaylist['items'])):
        if prePlaylist['items'][i]['name'] == playlistName:
            playlist = prePlaylist['items'][i]['id']

    #add songs to playlist
    spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=songList)

def getPlaylists(username, spotifyObject):
    prePlaylist = spotifyObject.user_playlists(user=username)
    playlistsName = []
    playlistsID = []
    for i in prePlaylist['items']:
        playlistsName.append(i['name'])
        playlistsID.append(i['id'])
    print(playlistsName)
    return playlistsName, playlistsID

def createSongList(playlistsID, playlistsName, spotifyObject):
    name = input('Which playlist are we looking at? ')
    ind = getIndex(name, playlistsName)
    result = spotifyObject.playlist(playlistsID[ind])
    songNames = []
    songIDs = []
    #print(json.dumps(result, indent=4))
    for i in range(len(result['tracks']['items'])):
        songNames.append(result['tracks']['items'][i]['track']['name'])
        songIDs.append(result['tracks']['items'][i]['track']['uri'])
    #print(songNames)
    print(json.dumps(songNames, indent=4))
    return songIDs

scope = 'playlist-modify-public'
#username = input('Enter your spotify username: ')
username = 'jamiesnyders'

token = SpotifyOAuth(scope=scope,username=username)
spotifyObject = spotipy.Spotify(auth_manager=token) #creates spotify object

#Names, IDs = getPlaylists(username, spotifyObject)
#print()
#songIDs = createSongList(IDs, Names, spotifyObject)

createPlaylist(username, spotifyObject)