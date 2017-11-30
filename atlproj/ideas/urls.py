from django.conf.urls import url, include
from . import views
from ideas.views import *
from atlproj.urls import *

urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url(r'^$', views.index, name='index'),
    url(r'^list/', include([
        url(r'^$', IdeaListView.as_view(), name='idea_list'),
        url(r'^current/$', CurrentIdeasView.as_view(), name='current_list'),
        url(r'^(?P<platform>[\w]+)/$', PlatformListView.as_view(), name='platform_idea_list'),
        url(r'^current/(?P<platform>[\w]+)/$', PlatformCurrentView.as_view(), name='platform_current_list'),
        ])),
    url(r'^(?P<pk>[0-9]+)/$', IdeaDetailView.as_view(), name='idea_detail'),
    url(r'^calendar/', include([
        url(r'^$', IdeaCalendarView.as_view(), name='calendar'),
        url(r'^calendar/(?P<platform>[\w]+)/$', PlatformCalendarView.as_view(), name='platform_calendar'),
        ])),
]