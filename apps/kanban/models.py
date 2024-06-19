from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Item(models.Model):
    board = models.ForeignKey(Board, related_name='item', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comments = models.IntegerField(default=0, blank=True)
    badge_text = models.CharField(max_length=50, blank=True)
    badge_color = models.CharField(max_length=20, blank=True)
    due_date = models.DateField(null=True, blank=True)
    attachments = models.IntegerField(default=0, blank=True)
    assigned = models.ManyToManyField(User, related_name='assigned_items', blank=True)
    members = models.ManyToManyField(User, related_name='member_items', blank=True)

    def __str__(self):
        return self.title


