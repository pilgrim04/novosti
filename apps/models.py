from django.db import models


class New(models.Model):
    source = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    date = models.DateTimeField()
    category = models.CharField(max_length=256)
    header = models.CharField(max_length=256)
    text = models.TextField()

