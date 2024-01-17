from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class URL(models.Model):
    # URL field to store the actual URL
    url = models.URLField(max_length=500)

    # ForeignKey to associate each URL with a User
    # on_delete=models.CASCADE tarkottaa if a User is deleted, their URLs will also be deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Boolean field to store whether the URL is malicious or not
    is_malicious = models.BooleanField(default=False)

    # DateTime field to store when the URL was checked
    # Automatically set to the time when the instance is created
    checked_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.url

