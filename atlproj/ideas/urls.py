from django.conf.urls import url, include
from . import views
from ideas.views import *
from atlproj.urls import *

urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url(r'^$', views.index, name='index'),
    url(r'^list/', include([
        url(r'^$', views.ideas_by_status, name='all_ideas'),
        url(r'^(?P<selector>[\w]+)/$', views.ideas_by_status, name='ideas_by_status'),
        url(r'^(?P<selector>[\w]+)/(?P<platform>[\w]+)/$', views.ideas_by_status, name='ideas_by_status'),
        ])),
    url(r'^flat/', include([
        url(r'^$', views.ideas_by_status, name='all_ideas_flattened'),
        url(r'^(?P<selector>[\w]+)/$', views.ideas_by_status, name='ideas_by_status_flattened'),
        url(r'^(?P<selector>[\w]+)/(?P<platform>[\w]+)/$', views.ideas_by_status, name='ideas_by_status_flattened'),
        ]), { 'flatten' : True, }),
    url(r'^available/', include([
        url(r'^$', IdeasList.as_view(), name='idea_list'),
        url(r'^(?P<platform>[\w]+)/$', PlatformIdeasList.as_view(), name='platform_idea_list'),
        ])),
    url(r'^active/', include([
        url(r'^$', CurrentIdeas.as_view(), name='current_list'),
        url(r'^(?P<platform>[\w]+)/$', PlatformCurrentIdeas.as_view(), name='platform_current_list'),
        ])),
    url(r'^complete/', include([
        url(r'^$', CompletedIdeas.as_view(), name='complete_list'),
        ])),
    url(r'^detail/', include([
        url(r'^(?P<pk>[0-9]+)/$', IdeaDetail.as_view(), name='idea_detail'),
        url(r'^(?P<pk>[0-9]+)/update/status/$', views.UpdateStatus, name='update_status'),
        ])),
    url(r'^tag/', include([
        url(r'^(?P<pk>[0-9]+)/$', TagDetail.as_view(), name='tag_detail'),
        ])),
    url(r'^calendar/', include([
        url(r'^$', IdeasCalendar.as_view(), name='calendar'),
        url(r'^calendar/(?P<platform>[\w]+)/$', PlatformCalendar.as_view(), name='platform_calendar'),
        ])),
    url(r'^pitches/', include([
        url(r'^$', PitchList.as_view(), name='pitch_list'),
        url(r'^sold/$', SoldPitches.as_view(), name='sold_pitches'),
        ])),
]