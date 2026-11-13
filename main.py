from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title(Author = "Ellie Welch", 
                 Description = "",
                 Planning = CS1_Final_Project_0.docx, CS1_Final_Project_1.docx ,
                 Link = ["https://github.com/lewelch/music-recs-deployment"])
set_website_framed(False)

music_data = "music_data_shortened.csv"
music_file = open(music_data, encoding ="utf-8")

music_info = []
for line in music_file:
    if line.strip() != ",track_id,artists,album_name,track_name,popularity,duration_ms,explicit,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,time_signature,track_genre":
        music_info.append(line.strip().split(","))
    
music_file.close()

songs = []
for song in music_info:
    if song[7] == "FALSE":
        new_song = []
        new_song.append(song[2])
        new_song.append(song[3])
        new_song.append(song[4])
        new_song.append(song[20])
        songs.append(new_song)

@dataclass
class Song():
    artist: str
    album: str
    title: str
    genre: str
    
@dataclass
class Album():
    title: str
    songs: list[Song]
    
@dataclass
class State():
    artist: str
    genre: str
    as_songs: bool
    albums: list[Album]
    saved_songs: list[Song]
    saved_albums: list[Album]
    
def create_songs(songs: list[list[str]]) -> list[Song]:
    """
    """
    new_songs = []
    for song in songs:
        new_songs.append(Song(song[0], song[1], song[2], song[3]))
    return new_songs
assert_equal(create_songs([["test","This is a test","Can You Tell?","Emo"]]), [Song("test", "This is a test", "Can You Tell?", "Emo")])

def create_albums(songs: list[Song]) -> list[Album]:
    """
    """
    new_albums = []
    for song in songs:
        in_album = False
        for album in new_albums:
            if song.album == album.title and song.artist == album.songs[0].artist:
                if song not in album.songs:
                    album.songs.append(song)
                in_album = True
        if not in_album:
            new_albums.append(Album(song.album, [song]))
    return new_albums

test_songs = [Song("test", "This is a test", "Can You Tell?", "Emo"), Song("test", "This is a test", "Hello?", "Emo"),
              Song("test", "This isn't a test", "See", "Emo"), Song(":D", "This is a test", "Yippee", "Pop")]
assert_equal(create_albums(test_songs),[Album("This is a test", [Song("test", "This is a test", "Can You Tell?", "Emo"), Song("test", "This is a test", "Hello?", "Emo")]),
                                          Album("This isn't a test", [Song("test", "This isn't a test", "See", "Emo")]),
                                          Album("This is a test", [Song(":D", "This is a test", "Yippee", "Pop")])])
SONGS = create_songs(songs)

ALBUMS = create_albums(SONGS)



@route
def index(state: State) -> Page:
    return Page(state, [Header("Music Recs!"),
                        "Enter your search criteria into the boxes below. \n",
                        "Artist:", TextBox("user_artist", state.artist),
                        "Genre:", TextBox("user_genre", state.genre),
                        Button("Search","search"), "\n", 
                        CheckBox("user_as_songs", state.as_songs), "Display as songs"])


def filter_artist(albums: list[Album], artist: str) -> list[Album]:
    filtered_albums = []
    for album in albums:
        if artist in album.songs[0].artist:
            filtered_albums.append(album)
    return filtered_albums
filter_test = [Album("", [Song("bug","","","pop"), Song("bug","","","rock")]), Album("",[Song("fly","","","rock")]),
               Album("", [Song("ick","","","jazz")]), Album("", [Song("bug;fly", "","","rock")])]

assert_equal(filter_artist(filter_test, "fly"), [Album("",[Song("fly","","","rock")]), Album("", [Song("bug;fly", "","","rock")])])
def filter_genre(albums: list[Album], genre: str) -> list[Album]:
    filtered_albums = []
    for album in albums:
        for song in album.songs:
            if genre == song.genre:
                filtered_albums.append(album)
    return filtered_albums

assert_equal(filter_genre(filter_test, "rock"),[Album("", [Song("bug","","","pop"), Song("bug","","","rock")]), Album("",[Song("fly","","","rock")]),
                                                  Album("", [Song("bug;fly", "","","rock")])])
@route
def search(state: State, user_artist: str, user_genre: str, user_as_songs: bool) -> Page:
    state.artist = user_artist
    state.genre = user_genre
    state.as_songs = user_as_songs
    if state.artist:
        state.albums = filter_artist(state.albums, state.artist)
    if state.genre:
        state.albums = filter_genre(state.albums, state.genre)
    if not state.albums:
        return Page(state,[Header("NO RESULTS :("),
                           "No music was found that matched your search criteria. Please try a different option. \n",
                           Button("Back", "to_home")])
    else:
        
        results = ""
        if state.as_songs:
            songs_results = []
            for album in state.albums:
                for song in album.songs:
                    songs_results.append(song)
            if len(song_results) >= 10:
                for i in range(10):
                    results += songs_results[i].title + " by " + songs_results[i].artist + "\n"
            else:
                for song in song_results:
                    results += song.title + " by " + song.artist + "\n"
        else:
            if len(state.albums) >= 10:
                for i in range(10):
                    results += state.albums[i].title + " by " + state.albums[i].songs[0].artist + "\n"
            else:
                for album in state.albums:
                    results += album.title + " by " + album.songs[0].artist + "\n"
        return Page(state, [Header("Results:"),
                            (results),
                            Button("Back", "to_home")])

@route
def to_home(state: State) -> Page:
    state.albums = ALBUMS
    return index(state)

start_server(State("","", False, ALBUMS,[],[]))
