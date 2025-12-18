from django.contrib import admin

from .models import Person, School, SchoolGroup

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'address')
    search_fields = ('school_name', 'address')

@admin.register(SchoolGroup)
class SchoolGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'school')
    search_fields = ('group_name',)