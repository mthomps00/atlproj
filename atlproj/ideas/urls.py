from django.conf.urls import url
from . import views
from ideas.views import IdeaListView, IdeaDetailView, IdeaCalendarView, IdeaYearView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', IdeaListView.as_view(), name='idea_list'),
    url(r'^(?P<pk>[0-9]+)/$', IdeaDetailView.as_view(), name='idea_detail'),
    url(r'^calendar/$', IdeaCalendarView.as_view(), name='calendar'),
    url(r'^year/(?P<year>[0-9]{4})/$', IdeaYearView.as_view(), name='year'),

]