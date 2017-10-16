from django.db import models
from datetime import date

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name

class Idea(models.Model):
    STATUSES = (
        ('ON_OFFER', 'On offer'),
        ('LIVE', 'Live'),
        ('COMMITTED', 'Committed'),
        ('ARCHIVED', 'Archived'),
        ('COMPLETED', 'Completed'),
    )
    short_title = models.CharField(max_length=255)
    marketing_title = models.CharField(max_length=255, blank=True)
    editorial_title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    date_submitted = models.DateField('date submitted', default=date.today)
    date_updated = models.DateField('last updated', auto_now=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUSES, default='ON_OFFER')
    deliverables = models.CharField(max_length=255, blank=True)
    start_date = models.DateField('start date', null=True, blank=True)
    end_date = models.DateField('end date', null=True, blank=True)
    length = models.PositiveSmallIntegerField(null=True, blank=True, help_text="How many weeks would this last?")
    lead_time = models.PositiveSmallIntegerField(null=True, blank=True, help_text="How many weeks of advance notice does this require?")
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    budget = models.PositiveIntegerField(null=True, blank=True)
    platform = models.ForeignKey(Platform, blank=True, null=True, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        if self.editorial_title:
            return self.editorial_title
        else:
            return self.short_title

class Pitch(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateField('date created', default=date.today)
    date_updated = models.DateField('last updated', auto_now=True)

    def __str__(self):
        name = "%s: %s" % (self.idea, self.client)
        return name
        
    class Meta:
        verbose_name_plural = "pitches"