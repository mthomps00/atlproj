from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import datetime
from django.http import HttpResponse, Http404
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView
from django.views.generic.edit import UpdateView
from ideas.models import Idea, Client, Pitch, Platform, Tag
from ideas.forms import IdeaStatus
from collections import OrderedDict

#################
# REGULAR VIEWS #
#################

@login_required
def index(request):
    today = datetime.today()
    ideas_list = Idea.objects.filter(status='ON_OFFER').order_by('-date_updated').filter(parent__isnull=True)[:10]
    active_ideas = Idea.objects.filter(status='LIVE').filter(start_date__lte=today).exclude(end_date__lte=today).order_by('-start_date')[:10]
    need_start_dates = Idea.objects.filter(status='COMMITTED').filter(start_date__isnull=True)
    calendar = Idea.objects.filter(start_date__gte=today).exclude(status='COMMITTED').order_by('start_date')[:25]
    
    # These three QuerySets are to combine a few types of ideas that need to be updated
    live_after_end_date = Idea.objects.filter(status='LIVE').filter(end_date__lte=today)
    not_live_after_start_date = Idea.objects.filter(status='SCHEDULED').filter(start_date__lte=today)
    committed_with_start_date = Idea.objects.filter(status='COMMITTED').filter(start_date__isnull=False)
    need_updates = live_after_end_date | not_live_after_start_date | committed_with_start_date

    platforms = Platform.objects.all()
    context = {
        'platforms': platforms,
        'calendar': calendar,
        'active_ideas': active_ideas,
        'ideas_list': ideas_list,
        'need_updates': need_updates,
        'need_start_dates': need_start_dates,
    }
    return render(request, 'ideas/index.html', context)
    
def home(request):
    today = datetime.today()
    active_ideas = Idea.objects.filter(status='LIVE').filter(start_date__lte=today).exclude(end_date__lte=today).order_by('-start_date')
    calendar = Idea.objects.filter(status='SCHEDULED').filter(start_date__gte=today).order_by('start_date')
    context = {
        'calendar': calendar,
        'active_ideas': active_ideas,
    }
    return render(request, 'ideas/home.html', context)

@login_required
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

@login_required
def ideas_by_status(request, selector='all', platform=False, flatten=False):
    today = datetime.today()
    status = {
        'draft': ('Not yet available', Idea.objects.filter(status='DRAFT').order_by('-end_date')),
        'available': ('Available to pitch', Idea.objects.filter(status='ON_OFFER').order_by('start_date', '-date_updated')),
        'committed': ('Committed, but not yet scheduled', Idea.objects.filter(status='COMMITTED').order_by('start_date')),
        'scheduled': ('Committed and scheduled', Idea.objects.filter(status='SCHEDULED').order_by('start_date', '-date_updated')),
        'active': ('Active now', Idea.objects.filter(status='LIVE').exclude(end_date__lte=today).order_by('start_date', '-date_updated')),
        'complete': ('Already completed', Idea.objects.filter(status='COMPLETED').order_by('-end_date')),
        'archived': ('No longer available', Idea.objects.filter(status='ARCHIVED').order_by('-end_date')),
        'all': ('All ideas', Idea.objects.all()),
    }
    
    try:
        ideas = status[selector][1]
    except:
        raise Http404("That is not a valid status.")
    
    if platform:
        platform = get_object_or_404(Platform, name=platform)
        ideas = ideas.filter(platform=platform)

    display_name = status[selector][0]
    
    if not request.user.groups.filter(name='Editorial'):
        ideas = ideas.exclude(status='DRAFT').exclude(status='ARCHIVED')
    
    if flatten == False:
        ideas = ideas.filter(parent__isnull=True)
    
    context = {
        'ideas': ideas,
        'platform': platform,
        'display_name': display_name,
        'selector': selector,
        'statuses': list(status),
        'flatten': flatten,
    }
    return render(request, 'ideas/ideas_flexlist.html', context)

#####################
# CLASS-BASED VIEWS #
#####################

class IdeasList(LoginRequiredMixin, ListView):
    queryset = Idea.objects.filter(parent__isnull=True).filter(status='ON_OFFER').order_by('start_date', '-date_updated')
    context_object_name = 'object_list'
    
class PitchList(LoginRequiredMixin, ListView):
    model = Pitch
    context_object_name = 'pitches'

class SoldPitches(LoginRequiredMixin, ListView):
    queryset = Pitch.objects.filter(status='SUCCESS').exclude(idea__status='LIVE').exclude(idea__status='COMPLETED')
    template_name = 'ideas/pitch_list.html'
    context_object_name = 'pitches'

    def get_context_data(self, **kwargs):
        context = super(SoldPitches, self).get_context_data(**kwargs)
        context['sold'] = True
        return context

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
    
class AllIdeas(LoginRequiredMixin, ListView):
    today = datetime.today()
    queryset = Idea.objects.all()
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(AllIdeas, self).get_context_data(**kwargs)
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
    
class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag