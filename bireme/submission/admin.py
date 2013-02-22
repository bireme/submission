from django.contrib import admin
from models import *

class GenericAdmin(admin.ModelAdmin):
    exclude = ('created', 'creator', 'updated', 'updater')

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'updater') and hasattr(obj, 'creator'):
            if change:
                obj.updater = request.user
            else:
                obj.creator = request.user
                obj.updater = request.user
        obj.save()

class StepLocalAdmin(admin.StackedInline):
    model = StepLocal
    extra = 0
    exclude = ('created', 'creator', 'updated', 'updater')

class BibliographicTypeLocalAdmin(admin.StackedInline):
    model = BibliographicTypeLocal
    extra = 0
    exclude = ('created', 'creator', 'updated', 'updater')

class StepAdmin(GenericAdmin):
    inlines = [StepLocalAdmin, ]
    
    list_display = ('title', 'parent', 'creator', 'created', 'updater', 'updated')
    list_filter = ('type', 'finish', 'pending')
    search_fields = ('title', )

class BibliographicTypeAdmin(GenericAdmin):
    list_display = ('title', 'creator', 'created', 'updater', 'updated')
    search_fields = ('title', )
    inlines = [BibliographicTypeLocalAdmin, ]

class TypeAdmin(GenericAdmin):
    list_display = ('title', 'creator', 'created', 'updater', 'updated')
    search_fields = ('title', )

class LildbiVersionAdmin(GenericAdmin):
    list_display = ('title', 'creator', 'created', 'updater', 'updated')
    search_fields = ('title', )    

class SubmissionAdmin(GenericAdmin):
    list_display = ('id', 'type', 'current_status', 'creator')
    search_fields = ('title', )
    list_filter = ('current_status', 'type')

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(FollowUp, GenericAdmin)
admin.site.register(LildbiVersion, LildbiVersionAdmin)
admin.site.register(BibliographicType, BibliographicTypeAdmin)
admin.site.register(TypeSubmission, GenericAdmin)