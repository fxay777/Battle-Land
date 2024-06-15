import pymongo
import json

client = pymongo.MongoClient("mongodb://root:w7KjHDzvLxzFDzgwGvXwbQAGDQCFh54kW8cK8NmF4m7JV3@51.222.245.4:27017/SGSoftware?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")

database = client["practice"]

player_col = database["profiles"]
leaderboard_col = database["leaderboards"]

def get_player(uuid):
    found = player_col.find_one({"uuid": uuid})
    return found

def get_leaderboard(ladder):
    found = leaderboard_col.find_one({"ladder": ladder})
    return found

def get_leaderboards():
    return list(leaderboard_col.find())