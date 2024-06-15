from django import template

register = template.Library()

@register.filter
def shorten(obj, int):
    arr = []

    for i in obj:
        arr.append(i)

    return arr[0:10]

@register.filter
def add(obj):
    return int(obj) + 1

@register.filter
def subtract(obj):
    return int(obj) - 1

@register.filter
def as_str(value):
    return str(value)

@register.filter
def split_data(data, page):
    min = (int(page) - 1) * 10
    max = ((int(page) - 1) * 10) + 10

    if (len(data) <= max):
        return data[min:]
    else:
        return data[min:max]


@register.filter
def correct_page(count, page):
    return ((int(page) - 1) * 10) + count 


@register.filter
def find_pagination(data):
    page = int(data)
    if page <= 4:
        return [1, 2, 3, 4, 5]
    else:
        min = page - 2
        max = page + 3

        data =[]

        for i in range(min, max):
            data.append(i)
        
        return data

@register.filter
def fix_counter(val, page):
    return int(val) + (int(page) - 1) * 10