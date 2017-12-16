from django.forms import ModelForm, RadioSelect
from django.forms import widgets
from ideas.models import Idea

class IdeaStatus(ModelForm):
    class Meta:
        model = Idea
        fields = ['status']
        widgets = {
            'status': RadioSelect(),
        }