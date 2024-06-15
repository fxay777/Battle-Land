import datetime
import json

from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render
from forums.models import Forum, Thread
from users.lib import core
from users.lib import kitmap as kits
from users.lib import practice as practice_lib
from users.lib import hcf
from users.models import User


def index(request):
    return render(request, 'index.html', {"news": Thread.objects.all()})

def trailer(request):
    return render(request, 'launches/trailer.html')


def practice(request):
    return render(request, 'leaderboards/practice.html',
                  {"data": practice_lib.get_leaderboards(), "selected_ladder": "NoDebuff", "page": "1"})


def kitmap(request):
    data = []

    kills = list(kits.players.find().sort("kills", -1).limit(10))
    k_s = {
        "display": "Most Kills",
        "stat": "kills",
        "data": kills
    }
    data.append(k_s)

    deaths = list(kits.players.find().sort('deaths', -1).limit(10))
    d_s = {
        "display": "Most Deaths",
        "stat": "deaths",
        "data": deaths
    }
    data.append(d_s)

    playtime = list(kits.players.find().sort('playtime', -1).limit(10))
    p_s = {
        "display": "Highest Playtime",
        "stat": "playtime",
        "data": playtime
    }
    data.append(p_s)

    lives = list(kits.players.find().sort("lives", -1).limit(10))
    l_s = {
        "display": "Top Lives",
        "stat": "lives",
        "data": lives
    }
    data.append(l_s)

    diamonds = list(kits.players.find().sort("ores.DIAMOND", -1).limit(10))
    di_s = {
        "display": "Most Diamonds Mined",
        "stat": 'diamonds',
        "data": diamonds
    }
    data.append(di_s)

    kdr = list(kits.players.find().sort("kdr", -1).limit(10))
    kdr_s = {
        "display": "Top KDR",
        "stat": 'kdr',
        "data": kdr
    }
    data.append(kdr_s)

    tokens = list(kits.players.find().sort("tokens", -1).limit(10))
    tokens_s = {
        "display": "Top Tokens",
        "stat": 'tokens',
        "data": tokens
    }
    data.append(tokens_s)

    return render(request, 'leaderboards/kitmap.html', {"data": data, "selected_stat": "kills", "page": "1"})


def kitmap_more(request, stat, page):
    data = []
    n = int(page) * 10

    kills = list(kits.players.find().sort("kills", -1).limit(n))
    k_s = {
        "display": "Most Kills",
        "stat": "kills",
        "data": kills
    }
    data.append(k_s)

    deaths = list(kits.players.find().sort('deaths', -1).limit(n))
    d_s = {
        "display": "Most Deaths",
        "stat": "deaths",
        "data": deaths
    }
    data.append(d_s)

    playtime = list(kits.players.find().sort('playtime', -1).limit(n))
    p_s = {
        "display": "Highest Playtime",
        "stat": "playtime",
        "data": playtime
    }
    data.append(p_s)

    lives = list(kits.players.find().sort("lives", -1).limit(n))
    l_s = {
        "display": "Top Lives",
        "stat": "lives",
        "data": lives
    }
    data.append(l_s)

    diamonds = list(kits.players.find().sort("ores.DIAMOND", -1).limit(n))
    di_s = {
        "display": "Most Diamonds Mined",
        "stat": 'diamonds',
        "data": diamonds
    }
    data.append(di_s)

    kdr = list(kits.players.find().sort("kdr", -1).limit(n))
    kdr_s = {
        "display": "Top KDR",
        "stat": 'kdr',
        "data": kdr
    }
    data.append(kdr_s)

    tokens = list(kits.players.find().sort("tokens", -1).limit(10))
    tokens_s = {
        "display": "Top Tokens",
        "stat": 'tokens',
        "data": tokens
    }
    data.append(tokens_s)

    return render(request, 'leaderboards/kitmap.html', {"data": data, "selected_stat": stat, "page": page})


def practice_more(request, ladder, page):
    data = practice_lib.get_leaderboards()

    valid = False

    for lb in data:
        if lb["ladder"] == ladder:
            valid = True

    if not valid:
        raise Http404("Ladder does not exist")

    return render(request, 'leaderboards/practice.html', {"data": data, "selected_ladder": ladder, "page": page})



def hcf_faction(request, faction):
    faction = hcf.get_faction(name=faction)

    if not faction:
        return Http404("Faction not found!")

    return render(request, "faction/faction.html", {"faction": faction})


def hcf_view(request):
    data = []

    kills = list(hcf.players.find().sort("kills", -1).limit(10))
    k_s = {
        "display": "Most Kills",
        "stat": "kills",
        "data": kills
    }
    data.append(k_s)

    d_s = {
        "display": "Most Deaths",
        "stat": "deaths",
    }
    data.append(d_s)

    p_s = {
        "display": "Highest Playtime",
        "stat": "playtime",
    }
    data.append(p_s)

    l_s = {
        "display": "Top Lives",
        "stat": "lives"
    }
    data.append(l_s)

    di_s = {
        "display": "Most Diamonds Mined",
        "stat": 'diamonds',
    }
    data.append(di_s)

    kdr_s = {
        "display": "Top KDR",
        "stat": 'kdr',
    }
    data.append(kdr_s)

    return render(request, 'leaderboards/hcf.html', {"data": data, "selected_stat": "kills", "page": "1"})


def hcf_more(request, stat, page):
    data = []
    n = int(page) * 10

    k_s = {
        "display": "Most Kills",
        "stat": "kills",
    }
    if stat == "kills":
        k_s["data"] = list(hcf.players.find().sort("kills", -1).limit(n))

    data.append(k_s)

    d_s = {
        "display": "Most Deaths",
        "stat": "deaths",
    }
    if stat == "deaths":
        d_s["data"] = deaths = list(hcf.players.find().sort('deaths', -1).limit(n))
    data.append(d_s)

    p_s = {
        "display": "Highest Playtime",
        "stat": "playtime",
    }
    if stat == 'playtime':
        p_s["data"] = list(hcf.players.find().sort('playtime', -1).limit(n))
    data.append(p_s)

    l_s = {
        "display": "Top Lives",
        "stat": "lives",
    }
    if stat == "lives":
        l_s["data"] = list(hcf.players.find().sort("lives", -1).limit(n))
    data.append(l_s)

    di_s = {
        "display": "Most Diamonds Mined",
        "stat": 'diamonds',
    }
    if stat == "diamonds":
        di_s["data"] = list(hcf.players.find().sort("ores.DIAMOND", -1).limit(n))
    data.append(di_s)

    kdr_s = {
        "display": "Top KDR",
        "stat": 'kdr',
    }
    if stat == "kdr":
        kdr_s["data"] = list(hcf.players.find().sort("kdr", -1).limit(n))
    data.append(kdr_s)

    return render(request, 'leaderboards/hcf.html', {"data": data, "selected_stat": stat, "page": page})


def ranks(request):
    return render(request, 'admin/ranks.html', {"ranks": core.get_ranks})


def staff(request):
    ranks = ["Owner", "Developer", "Admin", "Moderator"]
    data = []

    for r_name in ranks: 
        players = list(core.player_col.find({"rankName": r_name}))
        segment = {
            "rank": core.get_rank(r_name),
            "players": players,
        }
        data.append(segment)

    return render(request, 'staff.html', {"data": data})


def famous(request):
    data = []

    youtuber = {
        "rank": core.get_rank("Youtuber"),
        "players": list(core.player_col.find({"webData.rank": "Youtuber"})),
    }

    data.append(youtuber)

    famous = {
        "rank": core.get_rank("Famous"),
        "players": list(core.player_col.find({"webData.rank": "Famous"})),
    }

    data.append(famous)

    famous = {
        "rank": core.get_rank("Partner"),
        "players": list(core.player_col.find({"webData.rank": "Partner"})),
    }

    data.append(famous)

    data = sorted(data, key=lambda k: k['rank'].get('priority', 0), reverse=True)
    return render(request, 'famous.html', {"data": data})


def graphs(request):
    ip = "dc-cafe62c56827.clover.gg"
    data = list(core.tracker.find({"ip": ip}))
    return render(request, 'admin/graphs.html', {"data": data, "ip": ip})


def get_graph(request, ip):
    data = list(core.tracker.find({"ip": "dc-cafe62c56827.clover.gg"}, {"_id", False}))
    return JsonResponse({"data": data})


def api(request):
    return JsonResponse(User.objects.filter())
