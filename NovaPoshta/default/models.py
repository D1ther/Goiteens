from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Warehouse(models.Model):
    title = models.CharField("Назва пункту", null=False)
    adress = models.CharField("Адреса", null=False)
    city = models.CharField("Місто", null=False)
    width = models.FloatField("Ширина", null=False, validators=
                            [MinValueValidator(-90), MaxValueValidator(90)])
    lenght = models.FloatField("Довжина", null=False, validators=
                            [MinValueValidator(-180), MaxValueValidator(180)])
    
    class Meta:
        verbose_name = "Пункт видачі"
        verbose_name_plural = "Пункти видачі"

class Parcel(models.Model):
    STATUSES_CHOISE = [
        ("created", "Створено"),
        ("on_way", "В дорозі"),
        ("arrived", "Прибув до пункту видачі"),
        ("issued", "Видано"),
    ]

    number = models.CharField("Номер посилки", null=False, unique=True)
    sender = models.CharField("Відправник", null=False)
    recipient = models.CharField("Отримувач", null=False)
    weight = models.FloatField("Вага", null=False)
    status = models.CharField("Статус", null=False, choices=STATUSES_CHOISE, default="created")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='parcels')

    class Meta:
        verbose_name = "Посилка"
        verbose_name_plural = "Посилки"

class ParcelStatusHistory(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField("Статус", choices=Parcel.STATUSES_CHOISE)
    time_edit = models.DateTimeField("Час зміни статусу", auto_now_add=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='status_history')

    class Meta:
        verbose_name = "Історія статусів посилки"
        verbose_name_plural = "Історії статусів посилок"

class Client(models.Model):
    name = models.CharField("Ім'я клієнта", null=False)
    surname = models.CharField("Прізвище клієнта", null=False)
    phone = models.CharField("Телефон", null=False, unique=True)
    email = models.EmailField("Email", null=True, unique=True)

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"
 
