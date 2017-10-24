from django.contrib import admin
from .models import Idea, Client, Pitch, Platform, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

class PitchInline(admin.TabularInline):
    model = Pitch
    
class ProfileInline(admin.TabularInline):
    model = Profile

class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['short_title', 'editorial_title', 'marketing_title', 'subtitle', 'description', 'date_submitted']}),
        ('Scope', {'fields': ['deliverables', 'budget', 'lead_time', 'length']}),
        ('Status', {'fields': ['status', 'start_date', 'end_date']}),
        ('Meta', {'fields': ['parent', 'platform', 'notes']}),
    ]
    list_display = ('short_title', 'marketing_title', 'date_updated', 'status', 'platform', 'start_date', 'end_date')
    list_filter = ('platform', 'date_updated', 'status')
    list_editable = ('status', 'marketing_title', 'platform')
    inlines = [
        PitchInline,
    ]

class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'nickname')
    list_editable = ('title', 'nickname')

class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInline,
    ]

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Pitch)
admin.site.register(Client)
admin.site.register(Platform, PlatformAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)