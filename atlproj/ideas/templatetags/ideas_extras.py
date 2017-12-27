from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 
    
@register.inclusion_tag('snippet_shortplatform.html')
def short_platform(item, *args, **kwargs):
    platform = item.platform
    if kwargs:
        display = kwargs['display']
    else:
        display = 'calendar'
    return {'platform': platform, 'display': display}
    
@register.inclusion_tag('snippet_platform.html')
def show_platform(item, *args, **kwargs):
    platform = item.platform
    if kwargs:
        selector = kwargs['selector']
    else:
        selector = item.get_selector()
    return {'platform': platform, 'selector': selector}
    
@register.inclusion_tag('snippet_ideachildren.html')
def idea_children(idea):
    children = idea.idea_set.all()
    return {'children': children}