import datetime

from django import template
from users.lib import *

register = template.Library()

@register.filter
def has_permission(user, perm):
    return user.has_permission(perm)


@register.filter
def fix_chat_color(color):
    return core.fix_chat_color(color)


@register.filter
def time_stamp(stamp):
    return datetime.datetime.fromtimestamp(stamp / 1e3)

@register.filter
def to_date(date):
    return date
    # return datetime.datetime.strptime(date, "%d/%m/%Y %H:%M%p")

@register.filter
def convert_playtime(time):
    seconds = time / 1000
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    months = days / 30
    years = months / 12

    if seconds < 60:
        return (str(int(seconds)) + " seconds")
    if minutes < 60:
        return (str(int(minutes)) + " minutes")
    if hours < 24:
        return (str(int(hours)) + " hours")
    if days < 24:
        return (str(int(days)) + " days")
    if months < 30:
        return (str(int(months)) + " months")
    if years < 12:
        return (str(int(years)) + " years")

    return "N/A"


@register.filter
def get_faction_name_hcf(uuid):
    faction = hcf.get_faction_from_uuid(uuid)
    if faction == None:
        return "N/A"
    return faction['name']


@register.filter
def get_faction_name_kitmap(uuid):
    faction = kitmap.get_faction_from_uuid(uuid)
    if faction == None:
        return "N/A"
    return faction['name']


@register.filter
def get_faction_hcf(uuid):
    faction = hcf.get_faction_from_uuid(uuid)
    return faction


@register.filter
def dict_to_list(dict):
    return dict.values()


@register.filter
def get_faction_kitmap(uuid):
    faction = kitmap.get_faction_from_uuid(uuid)
    return faction


@register.filter
def get_data_by_uuid(uuid):
    return core.get_player_by_uuid(uuid)


@register.filter
def get_data_from_dict(dict, data):
    return dict[data]