from django.db import models
from .libs import upload_to


class New(models.Model):
    source = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    date = models.DateTimeField()
    category = models.CharField(max_length=256)
    header = models.CharField(max_length=256)
    text = models.TextField()
    img = models.CharField(blank=True, max_length=1024)
    img1 = models.ImageField(upload_to=upload_to, null=True, blank=True)
    # ALTER TABLE apps_new ADD COLUMN img varchar(1024);
