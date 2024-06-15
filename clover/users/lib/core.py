import pymongo
import re

client = pymongo.MongoClient("mongodb://root:w7KjHDzvLxzFDzgwGvXwbQAGDQCFh54kW8cK8NmF4m7JV3@51.222.245.4:27017/SGSoftware?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")

database = client["SGSoftware"]
player_col = database["coreprofiles"]
rank_col = database["ranks"]

def get_player(name):
    found = player_col.find_one({"name": name})
    return found

def get_player_ignore_case(name):
    found = player_col.find_one({"name": re.compile('^' + re.escape(name) + '$', re.IGNORECASE)})
    return found

def get_player_by_uuid(uuid):
    found = player_col.find_one({"uuid": uuid})
    return found

def get_rank(name):
    found = rank_col.find_one({"name": name})
    return found

def get_rank_by_id(uuid):
    return rank_col.find_one({"uuid": uuid})

def get_default_rank():
    return rank_col.find_one({"name": "Default"})

def get_ranks():
    return list(rank_col.find())

def get_players():
    return list(player_col.find())

def fix_chat_color(color):
    if "c" in color:
        return "#FF5555"
    if "4" in color:
        return "#AA0000"
    if "6" in color:
        return "#FFAA00"
    if "e" in color:
        return "#FFFF55"
    if "2" in color:
        return "#00AA00"
    if "b" in color:
        return "#55FFFF"
    if "3" in color:
        return "#00AAAA"
    if "1" in color:
        return "#0000AA"
    if "9" in color:
        return "#5555FF"
    if "d" in color:
        return "#FF55FF"
    if "5" in color:
        return "#AA00AA"
    if "f" in color:
        return "#fff"
    if "7" in color:
        return "#AAAAAA"
    if "8" in color:
        return "#555555"
    if "0" in color:
        return "#000"
    if "a" in color:
        return "#54FF54"
    return "#AAAAAA"