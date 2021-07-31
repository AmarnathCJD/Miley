from .. import db
playlist = db.playlist

def add_song(id, song_name):
 _songs = playlist.find_one({"id": id})
 if _songs:
  songs = _songs.get("songs")
 else:
  songs = []
 songs.append(song_name)
 playlist.update_one({"id": id}, {"$set": {"songs": songs}})

def remove_song(id, song_name):
 _songs = playlist.find_one({"id": id})
 if _songs:
  songs = _songs.get("songs")
 else:
  songs = []
 if song_name in songs:
  songs.remove(song_name)
 playlist.update_one({"id": id}, {"$set": {"songs": songs}})

def get_playlist(id):
 _songs = playlist.find_one({"id": id})
 if _songs:
   return _songs.get("songs")
 return False

