from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class School(models.Model):
    school_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    persons = models.ManyToManyField(Person, related_name='schools')

    def __str__(self):
        return self.school_name
    
class SchoolGroup(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='groups')
    group_name = models.CharField(max_length=50)
    members = models.ManyToManyField(Person, related_name='groups')

    def __str__(self):
        return self.group_name