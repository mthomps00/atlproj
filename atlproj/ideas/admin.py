from django.contrib import admin
from .models import Idea, Client, Pitch, Platform, Profile, GDoc, Tag, Role
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

class PitchInline(admin.TabularInline):
    model = Pitch
    raw_id_fields = ('client',)

class ProfileInline(admin.TabularInline):
    model = Profile

class StakeholderInline(admin.TabularInline):
    model = Role
    extra = 1

class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['short_title', 'editorial_title', 'marketing_title', 'subtitle', 'description', 'date_submitted']}),
        ('Scope', {'fields': ['deliverables', 'budget', 'lead_time', 'length']}),
        ('Status', {'fields': ['status', 'start_date', 'end_date']}),
        ('Meta', {'fields': ['parent', 'platform', 'workday_title', 'notes', 'gdocs', 'tags']}),
        ('Presentation', {'fields': ['design', 'preview_url', 'live_url', 'slug']}),
    ]
    list_display = ('title', 'date_updated', 'status', 'platform', 'start_date', 'end_date')
    list_filter = ('platform', 'date_updated', 'status')
    list_editable = ('status', 'platform', 'start_date', 'end_date')
    raw_id_fields = ('parent',)
    filter_horizontal = ('gdocs', 'tags')
    search_fields = ['short_title', 'editorial_title', 'marketing_title', 'subtitle', 'description', 'parent__short_title', 'parent__editorial_title', 'parent__marketing_title']
    inlines = [
        PitchInline, StakeholderInline,
    ]

class PitchAdmin(admin.ModelAdmin):
    list_display = ('idea', 'client', 'status', 'sell_by', 'notes')
    list_editable = ('client', 'status', 'sell_by')
    raw_id_fields = ('idea', 'client')
    search_fields = ['idea__short_title', 'idea__editorial_title', 'idea__marketing_title', 'client__name', 'notes']

class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'nickname')
    list_editable = ('title', 'nickname')

class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInline,
    ]

class GDocAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'description')
    list_editable = ('url', 'description')
    search_fields = ['name', 'description']

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_editable = ('name', 'description')
    search_fields = ['name', 'description']

class ClientAdmin(admin.ModelAdmin):
    search_fields = ['name',]

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Pitch, PitchAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(GDoc, GDocAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Platform, PlatformAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)