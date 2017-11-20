from django.shortcuts import render, get_object_or_404
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView
from django.views.generic.edit import UpdateView
from ideas.models import Idea, Client, Pitch, Platform

today = datetime.today()

# Create your views here.
def index(request):
    ideas_list = Idea.objects.filter(status='ON_OFFER').order_by('-date_updated').filter(parent__isnull=True)
    active_ideas = Idea.objects.filter(status='LIVE').filter(start_date__lte=today).exclude(end_date__lte=today).order_by('-start_date')
    calendar = Idea.objects.filter(start_date__gte=today).order_by('start_date')
    platforms = Platform.objects.all()
    context = {
        'platforms': platforms,
        'calendar': calendar,
        'active_ideas': active_ideas,
        'ideas_list': ideas_list,
    }
    return render(request, 'ideas/index.html', context)
    
class IdeaListView(ListView):
    queryset = Idea.objects.filter(parent__isnull=True).filter(status='ON_OFFER').order_by('start_date', '-date_updated')
    context_object_name = 'object_list'
    
class CurrentIdeasView(ListView):
    queryset = Idea.objects.filter(parent__isnull=True).filter(status='LIVE').exclude(end_date__lte=today).order_by('start_date', '-date_updated')
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(CurrentIdeasView, self).get_context_data(**kwargs)
        context['current'] = True
        return context
    
class IdeaRetireView(ListView):
    queryset = Idea.objects.filter(status='LIVE').filter(end_date__lte=today).order_by('end_date')
    context_object_name = 'object_list'

class IdeaCalendarView(ListView):
    queryset = Idea.objects.filter(start_date__gte=today).order_by('start_date')
    template_name = 'ideas/calendar.html'
    context_object_name = 'object_list'

class PlatformCalendarView(ListView):
    template_name = 'ideas/calendar.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        self.platform = get_object_or_404(Platform, name=self.kwargs['platform'])
        return Idea.objects.filter(start_date__gte=today).order_by('start_date').filter(platform=self.platform)
        
    def get_context_data(self, **kwargs):
        context = super(PlatformCalendarView, self).get_context_data(**kwargs)
        context['platform'] = self.platform
        return context

class PlatformListView(ListView):
    template_name = 'ideas/idea_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        self.platform = get_object_or_404(Platform, name=self.kwargs['platform'])
        return Idea.objects.filter(status='ON_OFFER').order_by('-start_date', '-date_updated').filter(platform=self.platform)
        
    def get_context_data(self, **kwargs):
        context = super(PlatformListView, self).get_context_data(**kwargs)
        context['platform'] = self.platform
        return context

class PlatformCurrentView(ListView):
    template_name = 'ideas/idea_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        self.platform = get_object_or_404(Platform, name=self.kwargs['platform'])
        return Idea.objects.filter(status='LIVE').exclude(end_date__lte=today).order_by('-start_date', '-date_updated').filter(platform=self.platform)
        
    def get_context_data(self, **kwargs):
        context = super(PlatformCurrentView, self).get_context_data(**kwargs)
        context['platform'] = self.platform
        context['current'] = True
        return context

class IdeaDetailView(DetailView):
    model = Idea