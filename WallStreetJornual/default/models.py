from django.db import models

class User(models.Model):
    STATUSES = [
        ("admin", "ADMIN"),
        ("default", "DEFAULT")
    ]
    status = models.CharField(choices=STATUSES)
    username = models.CharField(max_length=255)

class Event(models.Model):
    STATUSES = [
        ("Чернетка", "draft"),
        ("Опубліковано", "published"),
        ("Завершено", "completed"),
        ("Архівувати", "archived")
    ]
    PRIORITIES = [
        ("low", "LOW"),
        ("medium", "MEDIUM"),
        ("high", "HIGH")
    ]

    priority = models.CharField(choices=PRIORITIES)
    status = models.CharField(choices=STATUSES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    