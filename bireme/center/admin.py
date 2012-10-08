from django.contrib import admin
from models import *

class CenterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Center, CenterAdmin)