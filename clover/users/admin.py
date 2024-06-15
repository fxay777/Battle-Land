from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserVisit)
admin.site.register(RegisterToken)
admin.site.register(User)