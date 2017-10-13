from django.shortcuts import render
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.dates import YearArchiveView
from ideas.models import Idea, Client, Pitch

today = datetime.today()

# Create your views here.
def index(request):
    ideas_list = Idea.objects.order_by('short_title')[:5]
    context = {
        'ideas_list': ideas_list,
    }
    return render(request, 'ideas/index.html', context)
    
def detail(request, idea_id):
    return HttpResponse("You're looking at idea #%s" % idea_id)
    
class IdeaListView(ListView):
    queryset = Idea.objects.filter(parent__isnull=True)
    context_object_name = 'object_list'

class IdeaCalendarView(ListView):
    queryset = Idea.objects.filter(start_date__gte=today).order_by('start_date')
    template_name = 'ideas/calendar.html'
    context_object_name = 'object_list'

class IdeaYearView(YearArchiveView):
    queryset = Idea.objects.all()
    template_name = 'ideas/year.html'
    context_object_name = 'calendar'
    date_field = 'start_date'
    make_object_list = True
    allow_future = True

class IdeaDetailView(DetailView):
    model = Idea