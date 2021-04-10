# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    content = models.TextField(null=False)
    options = models.TextField(null=False) # comma separated string of options
    max_time = models.SmallIntegerField(null=False)
    correct_option = models.CharField(max_length=200)

    def __str__(self):
        return self.content


class Snippet(models.Model):
    title = models.TextField(null=False)
    content = models.TextField(null=False)

    def __str__(self):
        return  self.title

