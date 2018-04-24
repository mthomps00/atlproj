from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
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
        verbose_name = "Related URL"
        verbose_name_plural = "Related URLs"
        
class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tag_detail', args=[str(self.pk)])

class IdeaStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    long_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    # How should ideas with this status be sorted by default on list pages?
    default_sort_order = models.CharField(max_length=255, blank=True, default='start_date')

    # Who can see ideas with this status?
    visible_to_sales = models.BooleanField(default=True)
    visible_to_marketing = models.BooleanField(default=True)
    visible_to_product = models.BooleanField(default=True)
    visible_to_editorial = models.BooleanField(default=True)

class Idea(models.Model):
    STATUSES = (
        ('DRAFT', 'Not yet approved'),
        ('ON_OFFER', 'Available to pitch'),
        ('TENTATIVE', 'Still tentative'),
        ('COMMITTED', 'Committed but not yet scheduled'),
        ('SCHEDULED', 'Committed and scheduled'),
        ('LIVE', 'Currently active'),
        ('ARCHIVED', 'Archived'),
        ('COMPLETED', 'Completed'),
    )
    DESIGNS = (
        ('BASIC', 'Basic'),
        ('DELUXE', 'Deluxe'),
        ('CUSTOM', 'Custom'),
    )
    
    # TOP-LEVEL: fields containing high-level metadata about the project
    marketing_title = models.CharField(max_length=255, blank=True)
    editorial_title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    date_submitted = models.DateField('date submitted', default=date.today)
    short_title = models.CharField(max_length=255, unique_for_year='date_submitted')
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
    slug = models.CharField(max_length=255, blank=True)
        
    # META: fields with related information on the project
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, blank=True, null=True, on_delete=models.CASCADE)
    workday_title = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    gdocs = models.ManyToManyField(GDoc, related_name="ideas", related_query_name="idea", blank=True)
    tags = models.ManyToManyField(Tag, related_name="ideas", related_query_name="idea", blank=True)
    stakeholders = models.ManyToManyField(User, through='Role')
    
    def calculate_budget(self):
        
        # start with the baseline budget
        if self.budget:
            budget = self.budget
        
        # if there's no baseline budget, assume that's 0
        else:
            budget = 0
        
        # if this idea includes other ideas, tabulate their budgets and add those to the total
        children = self.idea_set.all()
        for child in children:
            if child.budget:
                budget += child.budget
        return budget
    
    def get_earliest_start_date(self):
        "Uses the lead time to determine the earliest start date"
    
        # Probably need to move most of this code into the template, and make this function much neater.
        if self.status == "COMPLETED" or self.status == "LIVE":
            earliest_start_date = "This project is already live or completed."
        elif self.status == "ARCHIVED":
            earliest_start_date = "This project has been archived. Please consult edit about a status change before pitching."
        elif self.status == "COMMITTED" or self.status == "ON_OFFER":
            
            # this is the core of the function, and would be the only thing left in the neater version
            if self.lead_time:
                today = datetime.today()
                lt = timedelta(weeks=self.lead_time)
                calculated_date = today + lt
                verbose_calculated_date = calculated_date.strftime("%B %m, %Y")
                earliest_start_date = "The editorial team must be given a lead time of at least %s weeks from the point of commitment to launch this project. If it were committed today, the earliest start date for this project would be %s." % (self.lead_time, verbose_calculated_date)
            else:
                earliest_start_date = "The lead time for this project has not been defined. Please determine lead time before pitching."
        elif self.status == "SCHEDULED":
            if self.start_date:
                earliest_start_date = "The start date for this project is set: %s" % self.start_date.srftime("%B %m, %Y")
            else:
                earliest_start_date = "A start date for this project has been chosen, but isn't yet in the database."
        else:
            earliest_start_date = "This project is not yet ready to pitch. Please finalize details before pitching."
        return earliest_start_date

    def title(self):
        
        # by default, use the short title
        title = self.short_title
        
        # if there's an editorial title, use that as the main title
        if self.editorial_title:
            title = self.editorial_title
        
        # if there's a marketing title, show it in parentheses
        if self.marketing_title:
            title += " (%s)" % self.marketing_title
        return title
    
    # this function is about to be deprecated by the new IdeaStatus model
    def get_selector(self):
        
        selector_list = {
            'DRAFT': 'draft',
            'ON_OFFER': 'available',
            'SCHEDULED': 'scheduled',
            'COMMITTED': 'committed',
            'COMPLETED': 'complete',
            'LIVE': 'active',
            'ARCHIVED': 'archived',
        }
        
        try:
            selector_list[self.status]
            return selector_list[self.status]
        except:
            return 'all'

    def __str__(self):
        return self.title()
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('idea_detail', args=[str(self.pk)])
        
    def clean(self):
        # Don't allow scheduled entries to exist without start dates.
        if self.status == 'SCHEDULED' and self.start_date is None:
            raise ValidationError(_('If the idea\'s already scheduled, please add the start date or change the status to "Committed, but not yet scheduled."'))

class Role(models.Model):
    ROLES = (
        ('EL', 'Editorial Lead'),
        ('SL', 'Sales Lead'),
        ('PL', 'Product Lead'),
        ('ML', 'Marketing Lead'),
        ('S', 'Stakeholder'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    role = models.CharField(max_length=3, choices=ROLES, default='S')

    def __str__(self):
        name = "%s: %s (%s)" % (self.idea, self.user.username, self.get_role_display())
        return name
    
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

    ideas = models.ManyToManyField(Idea, through='IdeaPitched', related_name='pitches', related_query_name='pitch')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateField('date pitched', default=date.today)
    date_updated = models.DateField('last updated', auto_now=True)
    sell_by = models.DateField('sell_by', blank=True, null=True)
    status = models.CharField(max_length=15, choices=PITCH_STATUSES, default='DRAFT')
    notes = models.TextField(blank=True)

    def __str__(self):
        name = "%s: %s" % (self.client, self.date_created)
        return name
    
    class Meta:
        verbose_name_plural = "pitches"

class IdeaPitched(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    included = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return "%s to %s on %s" % (self.idea, self.pitch.client, self.pitch.date_updated)
    
    def deliverables(self):
        return self.idea.deliverables
    
    class Meta:
        verbose_name = "idea pitched"
        verbose_name_plural = "ideas pitched"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_platform = models.ForeignKey(Platform, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=kwargs.get('instance'))