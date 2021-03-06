from django.contrib import admin
from .models import Idea, Client, Pitch, StartDate, EndDate, IdeaDate, IdeaPitched, Platform, Profile, Link, Tag, Role
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

# Register your models here.

class IdeaPitchedInline(admin.StackedInline):
    model = IdeaPitched
    fields = (('idea', 'pitch', 'deliverables'), 'notes')
    readonly_fields = ('deliverables',)
    autocomplete_fields = ['idea', 'pitch']
    
class PitchInline(admin.TabularInline):
    model = Pitch

class ProfileInline(admin.TabularInline):
    model = Profile

class StartDateInline(admin.TabularInline):
    model = StartDate

class EndDateInline(admin.TabularInline):
    model = EndDate

class IdeaDateInline(admin.TabularInline):
    model = IdeaDate

class StakeholderInline(admin.TabularInline):
    model = Role
    extra = 1

class IdeaPitchedAdmin(admin.ModelAdmin):
    search_fields = ['idea__short_title', 'idea__editorial_title', 'idea__marketing_title', 'pitch__client__name', 'notes']
    autocomplete_fields = ['idea', 'pitch']

class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['short_title', 'editorial_title', 'marketing_title', 'subtitle', 'description', 'date_submitted', 'status', 'expiration_date']}),
        ('Scope', {'fields': ['deliverables', 'budget', 'lead_time', 'length']}),
        ('Meta', {'fields': ['parent', 'platform', 'creative_brief', 'workday_title', 'notes', 'links', 'tags']}),
        ('Presentation', {'fields': ['design', 'preview_url', 'live_url', 'slug']}),
    ]
    list_display = ('admintitle', 'status', 'platform', 'dates', 'expiration_date', 'date_updated')
    list_filter = ('status', 'platform', 'date_updated')
    list_editable = ('status', 'platform', 'expiration_date')
    raw_id_fields = ('parent',)
    filter_horizontal = ('links', 'tags')
    search_fields = ['short_title', 'editorial_title', 'marketing_title', 'subtitle', 'description', 'parent__short_title', 'parent__editorial_title', 'parent__marketing_title']
    inlines = [
        StartDateInline, EndDateInline, IdeaDateInline, IdeaPitchedInline, StakeholderInline,
    ]
    
    def get_queryset(self, request):
        qs = super(IdeaAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif not request.user.groups.filter(name='Editorial'):
            qs = qs.exclude(status='DRAFT').exclude(status='ARCHIVED')
        return qs
        
    def admintitle(self, obj):
        if obj.parent:
            return format_html(
                '<small style="text-transform: uppercase; color: #CCC">{}</small><br />{}',
                obj.parent,
                obj.title(),
                )
        else:
            return obj.title()
            
    def dates(self, obj):
        if obj.new_start_date:
            dates = obj.new_start_date.date.strftime("%-m/%d/%y")
        if obj.new_end_date:
            dates += " to %s" % (obj.new_end_date.date.strftime("%-m/%d/%y"))
        return dates

class PitchAdmin(admin.ModelAdmin):
    fields = ('id', 'client', 'status', 'date_updated', 'date_created', 'sell_by', 'notes')
    list_display = ('id', 'client', 'status', 'date_updated', 'date_created', 'sell_by', 'notes')
    list_editable = ('status', 'sell_by', 'date_created')
    list_display_links = ('id', 'client')
    readonly_fields = ('id', 'date_updated')
    filter_horizontal = ('ideas',)
    search_fields = ['ideas__idea__short_title', 'ideas__idea__editorial_title', 'ideas__idea__marketing_title', 'client__name', 'notes']
    autocomplete_fields = ['ideas', 'client']
    inlines = [
        IdeaPitchedInline,
    ]

class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'nickname')
    list_editable = ('title', 'nickname')

class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInline,
    ]

class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'description')
    list_editable = ('url', 'description')
    search_fields = ['name', 'description']

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_editable = ('name', 'description')
    search_fields = ['name', 'description']

class ClientAdmin(admin.ModelAdmin):
    inlines = [
        PitchInline,
    ]
    search_fields = ['name',]

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Pitch, PitchAdmin)
admin.site.register(IdeaPitched, IdeaPitchedAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Platform, PlatformAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)