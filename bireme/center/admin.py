from django.contrib import admin
from models import *

class CenterAdmin(admin.ModelAdmin):
    search_fields = ["name", "code"]

class ExternalDatabaseAdmin(admin.ModelAdmin):
    search_fields = ["name", 'email', "center"]

admin.site.register(Center, CenterAdmin)
admin.site.register(ExternalDatabase, ExternalDatabaseAdmin)