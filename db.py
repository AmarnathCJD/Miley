from os import environ as e

db_url = e.get("MONGO_DB_URI")
from pymongo import MongoClient

db = (MongoClient (db_url))["Rylee"]
playlist = db.playlist


def update_playlist(mode="add", chat_id, song):
   _songs = playlist.find_one({"chat_id": chat_id})
   if _songs:
     songs = _songs.get("songs")
   else:
     songs = []
   if mode == "add":
     songs.append(song)
   elif mode == "remove":
     songs.remove(song)
   elif mode == "clear":
     songs = []
   playlist.update_one({"chat_id": chat_id}, {"$set": {"songs": songs}}, upsert=True)

def get_playlist(chat_id):
   _songs = playlist.find_one({"chat_id": chat_id})
   if _songs:
     songs = _songs.get("songs")
   else:
     songs = None
   return songs
