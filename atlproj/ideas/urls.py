from django.conf.urls import url, include
from . import views
from ideas.views import *
from atlproj.urls import *

urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url(r'^$', views.index, name='index'),
    url(r'^list/', include([
        url(r'^$', IdeasList.as_view(), name='idea_list'),
        url(r'^current/$', CurrentIdeas.as_view(), name='current_list'),
        url(r'^(?P<platform>[\w]+)/$', PlatformIdeasList.as_view(), name='platform_idea_list'),
        url(r'^current/(?P<platform>[\w]+)/$', PlatformCurrentIdeas.as_view(), name='platform_current_list'),
        ])),
    url(r'^(?P<pk>[0-9]+)/$', IdeaDetail.as_view(), name='idea_detail'),
    url(r'^calendar/', include([
        url(r'^$', IdeasCalendar.as_view(), name='calendar'),
        url(r'^calendar/(?P<platform>[\w]+)/$', PlatformCalendar.as_view(), name='platform_calendar'),
        ])),
]