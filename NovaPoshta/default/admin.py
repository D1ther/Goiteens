from django.contrib import admin
from . import models

@admin.register(models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Parcel)
class ParcelAdmin(admin.ModelAdmin):
    ...

@admin.register(models.ParcelStatusHistory)
class ParcelStatusHistoryAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    ...
