from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views
from ideas.views import *
from atlproj.urls import *

urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url(r'^$', views.index, name='index'),
    url(r'^agenda$', views.agenda, name='agenda'),
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
    url(r'^calendar/', include([
        url(r'^$', views.ideas_by_date, name='calendar'),
        url(r'^(?P<platform>[\w]+)/$', views.ideas_by_date, name='platform_calendar'),
        ])),
    url(r'^detail/', include([
        url(r'^(?P<pk>[0-9]+)/$', IdeaDetail.as_view(), name='idea_detail'),
        url(r'^(?P<pk>[0-9]+)/update/status/$', views.UpdateStatus, name='update_status'),
        url(r'^(?P<pk>[0-9]+)/update/$', UpdateIdea.as_view(), name='update_idea'),
        ])),
    url(r'^tag/', include([
        url(r'^(?P<pk>[0-9]+)/$', TagDetail.as_view(), name='tag_detail'),
        ])),
    url(r'^pitches/', include([
        url(r'^$', PitchList.as_view(), name='pitch_list'),
        url(r'^sold/$', SoldPitches.as_view(), name='sold_pitches'),
        ])),
    url(r'^secret/', include([
        url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='secret_login'),
        ])),
]