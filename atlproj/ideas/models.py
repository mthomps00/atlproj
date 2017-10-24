from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date, datetime, timedelta
from django.dispatch import receiver

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    nickname = models.CharField(max_length=20, blank=True)
    
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
    
    def get_earliest_start_date(self):
        "Uses the lead time to determine the earliest start date"
    
        if self.status == "COMPLETED" or self.status == "LIVE":
            earliest_start_date = "This project is already live or completed."
        elif self.status == "ARCHIVED":
            earliest_start_date = "This project has been archived. Please consult edit about a status change before pitching."
        elif self.status == "COMMITTED" or self.status == "ON_OFFER":
            if self.lead_time:
                today = datetime.today()
                lt = timedelta(weeks=self.lead_time)
                calculated_date = today + lt
                verbose_calculated_date = calculated_date.strftime("%B %m, %Y")
                earliest_start_date = "The earliest start date for this project is %s." % verbose_calculated_date
            else:
                earliest_start_date = "The lead time for this project has not been defined. Please determine lead time before pitching."
        else:
            earliest_start_date = "This project is not yet ready to pitch. Please finalize details before pitching."
        return earliest_start_date

    
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
    sell_by = models.DateField('sell_by', blank=True, null=True)

    def __str__(self):
        name = "%s: %s" % (self.idea, self.client)
        return name
    
    class Meta:
        verbose_name_plural = "pitches"
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_platform = models.ForeignKey(Platform, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class GDoc(models.Model):
    name = models.CharField(max_length=255)
    ideas = models.ManyToManyField(Idea, related_name="gdocs", related_query_name="gdoc", blank=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
        
    
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=kwargs.get('instance'))