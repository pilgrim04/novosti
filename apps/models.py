from django.db import models


class New(models.Model):
    source = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    date = models.DateTimeField()
    category = models.CharField(max_length=256)
    header = models.CharField(max_length=256)
    text = models.TextField()
    img = models.CharField(blank=True, max_length=1024)
    # ALTER TABLE apps_new ADD COLUMN img varchar(1024);
