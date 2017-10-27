from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 
    
@register.inclusion_tag('snippet_shortplatform.html')
def short_platform(item):
    platform = item.platform
    return {'platform': platform}
    
@register.inclusion_tag('snippet_ideachildren.html')
def idea_children(idea):
    children = idea.idea_set.all()
    return {'children': children}