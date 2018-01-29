from django import forms
from django.forms import widgets
from ideas import models
from ideas.models import Idea

class IdeaStatus(forms.ModelForm):
    update_children = forms.BooleanField()
    
    class Meta:
        model = Idea
        fields = ['status', 'update_children']
        widgets = {
            'status': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'update_children': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UpdateIdea(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['short_title', 'status']