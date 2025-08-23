from django.db import models

class Category(models.Model):
    TITLES = [
        ("Навчання", "learning"),
        ("Розваги", "entertainment"),
        ("Спорт", "sports"),
        ("Новини", "news"),
    ]
    title = models.CharField(max_length=100, choices=TITLES)

class Subscription(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    content = models.ManyToOneRel(field="Content", field_name="subscribe", to="Content")

class User(models.Model):
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=32)
    

    subscribes = models.ManyToManyField(Subscription)

class Content(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()


class UserSubscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribe = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)