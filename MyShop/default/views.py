from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about_me.html')

def tables(request):
    return render(request, 'tables.html')