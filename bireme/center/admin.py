from django.contrib import admin
from models import *

class CenterAdmin(admin.ModelAdmin):
    search_fields = ["name", "code"]

admin.site.register(Center, CenterAdmin)