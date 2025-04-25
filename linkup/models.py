from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_events')
    participants = models.ManyToManyField(User, related_name='events_participating')

    def __str__(self):
        return self.title
