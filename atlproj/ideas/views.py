from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView
from django.views.generic.edit import UpdateView
from ideas.models import Idea, Client, Pitch, Platform
from ideas.forms import IdeaStatus

#################
# REGULAR VIEWS #
#################

@login_required
def index(request):
    today = datetime.today()
    ideas_list = Idea.objects.filter(status='ON_OFFER').order_by('-date_updated').filter(parent__isnull=True)[:10]
    active_ideas = Idea.objects.filter(status='LIVE').filter(start_date__lte=today).exclude(end_date__lte=today).order_by('-start_date')[:10]
    calendar = Idea.objects.filter(start_date__gte=today).order_by('start_date')[:25]
    platforms = Platform.objects.all()
    context = {
        'platforms': platforms,
        'calendar': calendar,
        'active_ideas': active_ideas,
        'ideas_list': ideas_list,
    }
    return render(request, 'ideas/index.html', context)
    
def home(request):
    today = datetime.today()
    active_ideas = Idea.objects.filter(status='LIVE').filter(start_date__lte=today).exclude(end_date__lte=today).order_by('-start_date')
    calendar = Idea.objects.filter(status='COMMITTED').filter(start_date__gte=today).order_by('start_date')
    context = {
        'calendar': calendar,
        'active_ideas': active_ideas,
    }
    return render(request, 'ideas/home.html', context)

def UpdateStatus(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    if request.method == 'POST':
        form = IdeaStatus(request.POST, instance=idea)
        if form.is_valid():
            form.save()
    else:
        form = IdeaStatus()
    
    context = {
        'form': form,
        'idea': idea,
    }    
    
    return render(request, 'ideas/update_status.html', context)


#####################
# CLASS-BASED VIEWS #
#####################

class IdeasList(LoginRequiredMixin, ListView):
    queryset = Idea.objects.filter(parent__isnull=True).filter(status='ON_OFFER').order_by('start_date', '-date_updated')
    context_object_name = 'object_list'
    
class CurrentIdeas(LoginRequiredMixin, ListView):
    today = datetime.today()
    queryset = Idea.objects.filter(parent__isnull=True).filter(status='LIVE').exclude(end_date__lte=today).order_by('start_date', '-date_updated')
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(CurrentIdeas, self).get_context_data(**kwargs)
        context['current'] = True
        return context
    
class CompletedIdeas(LoginRequiredMixin, ListView):
    today = datetime.today()
    queryset = Idea.objects.filter(parent__isnull=True).filter(status='COMPLETED').order_by('-end_date')
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(CompletedIdeas, self).get_context_data(**kwargs)
        context['complete'] = True
        return context
    
class IdeaRetire(LoginRequiredMixin, ListView):
    today = datetime.today()
    queryset = Idea.objects.filter(status='LIVE').filter(end_date__lte=today).order_by('end_date')
    context_object_name = 'object_list'

class IdeasCalendar(LoginRequiredMixin, ListView):
    today = datetime.today()
    queryset = Idea.objects.filter(start_date__gte=today).order_by('start_date')
    template_name = 'ideas/calendar.html'
    context_object_name = 'object_list'

class PlatformCalendar(LoginRequiredMixin, ListView):
    template_name = 'ideas/calendar.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        today = datetime.today()
        self.platform = get_object_or_404(Platform, name=self.kwargs['platform'])
        return Idea.objects.filter(start_date__gte=today).order_by('start_date').filter(platform=self.platform)
        
    def get_context_data(self, **kwargs):
        context = super(PlatformCalendar, self).get_context_data(**kwargs)
        context['platform'] = self.platform
        return context

class PlatformIdeasList(LoginRequiredMixin, ListView):
    template_name = 'ideas/idea_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        self.platform = get_object_or_404(Platform, name=self.kwargs['platform'])
        return Idea.objects.filter(status='ON_OFFER').order_by('-start_date', '-date_updated').filter(platform=self.platform)
        
    def get_context_data(self, **kwargs):
        context = super(PlatformIdeasList, self).get_context_data(**kwargs)
        context['platform'] = self.platform
        return context

class PlatformCurrentIdeas(LoginRequiredMixin, ListView):
    template_name = 'ideas/idea_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        today = datetime.today()
        self.platform = get_object_or_404(Platform, name=self.kwargs['platform'])
        return Idea.objects.filter(status='LIVE').exclude(end_date__lte=today).order_by('-start_date', '-date_updated').filter(platform=self.platform)
        
    def get_context_data(self, **kwargs):
        context = super(PlatformCurrentIdeas, self).get_context_data(**kwargs)
        context['platform'] = self.platform
        context['current'] = True
        return context

class IdeaDetail(LoginRequiredMixin, DetailView):
    model = Idea
