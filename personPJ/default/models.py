from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birthday = models.DateField()
    age = models.IntegerField()
    mail = models.CharField(max_length=100)