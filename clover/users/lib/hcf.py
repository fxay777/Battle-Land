import pymongo
import json
import re

client = pymongo.MongoClient("mongodb://localhost:27017")

database = client["armadas"]

players = database["profiles"]
p_factions = database["playerfactions"]

def get_player(uuid):
    found = players.find_one({"uuid": uuid})
    return found

def get_faction(name):
    found = p_factions.find_one({"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)})
    return found

def get_faction_from_uuid(uuid):
    found = p_factions.find_one({"uuid": uuid})
    return found


def get_players():
    return list(players.find())
