from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Forum)
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(ThreadReply)
admin.site.register(ThreadTag)