# from django.db import models
# from django.contrib.auth.models import User

# class Event(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_events')
#     participants = models.ManyToManyField(User, related_name='events_participating')

#     def __str__(self):
#         return self.title

# linkup/models.py
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

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')

    def __str__(self):
        return f'{self.user.username} - {self.friend.username}'

# class Friend(models.Model):
#     # The user who sent the friend request
#     from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
#     # The user who received the friend request
#     to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
#     # The status of the request
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#     )
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

#     def __str__(self):
#         return f'{self.from_user} -> {self.to_user} ({self.status})'
    
#     class Meta:
#         unique_together = ('from_user', 'to_user')  # Ensure each pair is unique