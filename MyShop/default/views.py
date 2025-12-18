from django.shortcuts import render

from .models import Person, School, SchoolGroup

def home(request):
    return render(request, 'index.html')

def about(request):
    persons = Person.objects.all()
    
    return render(request, 'about_me.html', {'persons': persons})

def tables(request):
    return render(request, 'tables.html')
