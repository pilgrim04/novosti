__author__ = 'korvin'
# -*- coding: utf-8 -*-
from hashlib import md5
from time import time
from os import path as op
import urllib2
from django.core.files.base import ContentFile
from django.utils import timezone

def upload_to(instance, filename, prefix=None, unique=True):
    ext = op.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time()) if unique else '')
    filename = md5(name.encode('utf8')).hexdigest() + ext
    date_path = str(timezone.now().year) + '/' + str(timezone.now().month) + '/' + str(timezone.now().day)
    basedir = op.join(instance._meta.app_label, instance._meta.module_name, date_path)

    if prefix:
        print 'prefix!!!'
        basedir = op.join(instance._meta.app_label, instance._meta.module_name, prefix)

    return op.join(basedir, filename)




def download_file(instance, field, url, save=False):
    """
    Загрзка фотографии по урлу
    :param instance: Instance of Model
    :param field: Name of field (FileField, ImageField) (передавать в str)
    :param url: url of desired file
    :param save: save after upload
    """
    try:
        url = urllib2.urlopen(url)
        filename = url.geturl().split('/')[-1]
        getattr(instance, field).save(upload_to(instance, filename), ContentFile(url.read()), save=save)
    except urllib2.URLError:
        return False
    return True