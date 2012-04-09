from django.db import models
import re

from django.core.urlresolvers import reverse

class Task(models.Model):
    name = models.CharField(max_length=255)  
    domain = models.CharField(max_length=255)  
    allowed_domains = models.TextField(blank=True)
    description = models.TextField(blank=True)      
    start_urls = models.TextField()
    rules = models.TextField()
    priority = models.FloatField(default=0.0)
    
    created = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True)
    
    def next(self, **kwargs):
        qs = Task.objects.filter(**kwargs).order_by('priority')
        if qs:
            return qs[0]
        else:
            return None
        
    def load(self,id):
        return self.next(id=id)
    

class URLResult(models.Model):
    url = models.CharField(max_length=255)
    source_url = models.CharField(max_length=255)
    content = models.TextField()
    response_status = models.IntegerField()
    response_time = models.FloatField()
    content_length = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    # store any urls extracted from the content during spidering
    urls = []
    
    class Meta:
        ordering = ('source_url', 'url',)
    
    def __unicode__(self):
        return '%s [%s]' % (self.url, self.response_status)

    def get_absolute_url(self):
        return reverse('profiles_url_result_detail', args=[
            self.session.spider_profile_id, self.session_id, self.pk
        ])
    
    def previous_results(self):
        return URLResult.objects.filter(
            url=self.url,
            created_date__lt=self.created_date
        ).order_by('-created_date')
    
    def previous_status(self):
        previous_qs = self.previous_results()
        
        try:
            most_recent = previous_qs[0]
        except IndexError:
            return None
        else:
            return most_recent.response_status

    def short_url(self):
        return re.sub('^([a-z]+:\/\/)?([^\/]+)', '', self.url)

