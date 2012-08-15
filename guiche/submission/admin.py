from django.contrib import admin
from models import *

class GeneralAdmin(admin.ModelAdmin):
    
    exclude = ('created', 'updated', 'updater', 'creator')

    def save_model(self, request, obj, form, change):
        
        if hasattr(obj, 'updater') and hasattr(obj, 'creator'):
            if change:
                obj.updater = request.user
            else:
                obj.creator = request.user
                obj.updater = request.user

        obj.save()

class SubmissionAdmin(GeneralAdmin):
    list_display = ('type', 'creator', 'created', 'updater', 'updated')
    list_filter = ('status', )

admin.site.register(Submission, SubmissionAdmin)