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
    
    def nickcheck(self):
        if self.nickname:
            nickname = self.nickname
        else:
            nickname = self.name
            
        return nickname

class GDoc(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Google Doc"
        verbose_name_plural = "Google Docs"
        
class Idea(models.Model):
    STATUSES = (
        ('DRAFT', 'Not yet approved'),
        ('ON_OFFER', 'On offer'),
        ('TENTATIVE', 'Tentative'),
        ('LIVE', 'Live'),
        ('COMMITTED', 'Committed'),
        ('ARCHIVED', 'Archived'),
        ('COMPLETED', 'Completed'),
    )
    DESIGNS = (
        ('BASIC', 'Basic'),
        ('DELUXE', 'Deluxe'),
        ('CUSTOM', 'Custom'),
    )
    
    # TOP-LEVEL: fields containing high-level metadata about the project
    short_title = models.CharField(max_length=255)
    marketing_title = models.CharField(max_length=255, blank=True)
    editorial_title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    date_submitted = models.DateField('date submitted', default=date.today)
    date_updated = models.DateField('last updated', auto_now=True)
    description = models.TextField(blank=True)
    
    # SCOPE: fields about the size of the project and its deliverables
    deliverables = models.CharField(max_length=255, blank=True)
    length = models.PositiveSmallIntegerField(null=True, blank=True, help_text="How many weeks would this last?")
    lead_time = models.PositiveSmallIntegerField(null=True, blank=True, help_text="How many weeks of advance notice does this require?")
    budget = models.PositiveIntegerField(null=True, blank=True)

    # STATUS: fields about where the project stands
    status = models.CharField(max_length=15, choices=STATUSES, default='ON_OFFER')
    start_date = models.DateField('start date', null=True, blank=True)
    end_date = models.DateField('end date', null=True, blank=True)
    
    # PRESENTATION: fields about how/where the project will live publicly
    design = models.CharField(max_length=15, choices=DESIGNS, default='BASIC')
    preview_url = models.URLField(null=True, blank=True)
    live_url = models.URLField(null=True, blank=True)
        
    # META: fields with related information on the project
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, blank=True, null=True, on_delete=models.CASCADE)
    workday_title = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    gdocs = models.ManyToManyField(GDoc, related_name="gdocs", related_query_name="gdoc", blank=True)
    
    def calculate_budget(self):
        if self.budget:
            budget = self.budget
        else:
            budget = 0
        children = self.idea_set.all()
        for child in children:
            if child.budget:
                budget += child.budget
        return budget
    
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

    def title(self):
        title = self.short_title
        
        if self.editorial_title:
            title = self.editorial_title
        
        if self.marketing_title:
            title += " (%s)" % self.marketing_title
        
        return title
        
    def __str__(self):
        return self.title()
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('idea_detail', args=[str(self.pk)])

class Pitch(models.Model):
    PITCH_STATUSES = (
        ('DRAFT', 'Not yet pitched'),
        ('POSSIBLE', 'Under consideration'),
        ('LIKELY', 'Likely to succeed'),
        ('ALMOST', 'Very likely to succeed'),
        ('SUCCESS', 'Pitch succeeded'),
        ('UNLIKELY', 'Long shot'),
        ('DEAD', 'No go'),
    )

    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateField('date created', default=date.today)
    date_updated = models.DateField('last updated', auto_now=True)
    sell_by = models.DateField('sell_by', blank=True, null=True)
    status = models.CharField(max_length=15, choices=PITCH_STATUSES, default='DRAFT')
    notes = models.TextField(blank=True)

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

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=kwargs.get('instance'))