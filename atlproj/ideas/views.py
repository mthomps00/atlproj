from django.shortcuts import render, get_object_or_404
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView
from ideas.models import Idea, Client, Pitch, Platform

today = datetime.today()

# Create your views here.
def index(request):
    ideas_list = Idea.objects.filter(start_date__gte=today).order_by('start_date').filter(parent__isnull=True)
    active_ideas = Idea.objects.exclude(status='ARCHIVED').exclude(status='COMPLETED').filter(start_date__lte=today).filter(end_date__gte=today)
    platforms = Platform.objects.all()
    context = {
        'platforms': platforms,
        'active_ideas': active_ideas,
        'ideas_list': ideas_list,
    }
    return render(request, 'ideas/index.html', context)
    
class IdeaListView(ListView):
    queryset = Idea.objects.filter(parent__isnull=True)
    context_object_name = 'object_list'

class IdeaCalendarView(ListView):
    queryset = Idea.objects.filter(start_date__gte=today).order_by('start_date').filter(parent__isnull=True)
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

class IdeaDetailView(DetailView):
    model = Idea