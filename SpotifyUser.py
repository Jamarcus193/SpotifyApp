import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from Playlist import Playlist
import cred

class User:
    scope = 'playlist-modify-public'
    chosenPlaylist = None 

    def getIndex(self, lst):
        return lst.index()
    
    def importPlaylists(self):
        for i in self.playlistsJson['items']:
            self.playlistsName.append(i['name'])
            self.playlistsID.append(i['id'])
        #print(playlistsName)
        #print('\n'.join('{}: {}'.format(*k) for k in enumerate(playlistsID))) #print the elements of the list in a downwards line
        #print('\n'.join('{}: {}'.format(*k) for k in enumerate(zip(playlistsName, playlistsID))))
        #print(dict(zip(playlistsName, playlistsID)))
        return self.playlistsName, self.playlistsID

    def showData(self):
        print('\n'.join('{}: {}'.format(*k) for k in enumerate(self.playlistsName))) #print the elements of the list in a downwards line

    
    def createPlaylist(self):
        pName = input('\nnew playlist name is? ')
        descr = input('\nPlaylist description? ')
        self.spotifyObject.user_playlist_create(user=self.username, name=pName,public=True,description=descr)
        return pName
        
    def getPlaylistID(self, pName):
        prePlaylist = self.spotifyObject.user_playlists(user=self.username) #Get the playlists linked to spotify account
        for i in range(len(prePlaylist['items'])):
            if prePlaylist['items'][i]['name'] == pName:
                playlistID = prePlaylist['items'][i]['id']
        return playlistID

    def getSongList(self, name, playlistID, spotifyObject):
        result = spotifyObject.playlist(playlistID)
        songNames = []
        songIDs = []
        print('\n')
        for i in range(len(result['tracks']['items'])):
            songNames.append(result['tracks']['items'][i]['track']['name'])
            songIDs.append(result['tracks']['items'][i]['track']['uri'])
        print('\n'.join('{}: {}'.format(*k) for k in enumerate(songNames)))
        return songNames, songIDs

    def choosePlaylist(self):
        nameInd = int(input('\nInput the number of the playlist you would like to import from: '))
        pName = self.playlistsName[nameInd]
        songSubset = []
        idSubset = []
        print('\nYou selected the playlist titled: \n \t-> {}'.format(pName))
        if input('\nyes or no?\t') == 'yes':
            playlistID = self.getPlaylistID(pName)
            print(f'\nSongs found in {pName}')
            songNames, songList = self.getSongList(pName, playlistID, self.spotifyObject)

            print('\nInput song numbers until you have your desired subset and then type quit\n')
            user_input = input('Enter the song num: ')
            while user_input != 'quit':
                songSubset.append(user_input)
                user_input = input('Enter the song num: ')

            print('\nSongs you are importing: ')
            for i in songSubset:
               print('-------> {}'.format(songNames[int(i)]))
               idSubset.append(songList[int(i)])

            pName = self.createPlaylist()
            playlistID = self.getPlaylistID(pName)
            self.spotifyObject.user_playlist_add_tracks(user=self.username,playlist_id=playlistID,tracks=idSubset)
            print('Created playlist {} with the selected subset of songs :)'.format(pName))

    def start(self):
        print('\nYou are manipulating the {} spotify account'.format(self.username))
        print('Playlists found on the account\n')
        self.playlistsName, self.playlistsID = self.importPlaylists()
        self.showData()
        


    
    def __init__(self, username='jamiesnyders'):
        self.username = username
        self.token = SpotifyOAuth(client_id=cred.client_id, client_secret= cred.client_secret, redirect_uri=cred.redirect_url, scope=self.scope)
        self.spotifyObject = spotipy.Spotify(auth_manager=self.token)
        self.playlistsJson = self.spotifyObject.user_playlists(user=self.username)
        self.playlistsName = []
        self.playlistsID = []

    