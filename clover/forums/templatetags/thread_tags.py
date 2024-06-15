from django import template
from datetime import datetime

register = template.Library()

def get_suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + get_suffix(t.day))

@register.filter
def format_time(date):
    return custom_strftime('%b {S}, %Y', date)


@register.filter
def has_permission_to_create_thread(user, category):
    return user.has_permission('thread.create.' + category.name)

@register.filter
def short_ntime(date):
    now = datetime.now()
    time = now.timestamp() - date.timestamp()

    seconds = time
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    months = days / 30
    years = months / 12

    if seconds < 60:
        if (seconds == 1):
            return "1 second ago"
        return (str(int(seconds)) + " seconds ago")
    if minutes < 60:
        if minutes == 1:
            return "1 minute ago"
        return (str(int(minutes)) + " minutes ago")
    if hours < 24:
        if hours == 1:
            return "1 hour ago"
        return (str(int(hours)) + " hours ago")
    if days < 24:
        if days == 1:
            return "1 day ago"
        return (str(int(days)) + " days ago")
    if months < 30:
        if months == 1:
            return "1 month ago"
        return (str(int(months)) + " months ago")
    if years < 12:
        if year == 1:
            return "1 year ago"
        return (str(int(years)) + " years ago")

    return "N/A"