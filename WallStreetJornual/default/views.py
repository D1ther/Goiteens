from django.shortcuts import render
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage,
)

from .services.event import (
    get_events,
    create_event,
    edit_event
)

from . import forms

from . import models

def show_events(request):
    events = get_events(request.user.username)
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')

    try:
        events_page = paginator.get_page(page_number)
    except PageNotAnInteger:
        events_page = paginator.get_page(1)
    except EmptyPage:
        events_page = paginator.get_page(paginator.num_pages)

    return render(
        request,
        "events.html",
        {
            "events": events_page,
            "paginator": paginator
        }
    )

def add_event(request):
    if request.method == "POST":
        form = forms.CreateEventForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            event = create_event(
                title=data["title"],
                description=data["description"],
                date={
                    "year": data["date"].year,
                    "month": data["date"].month,
                    "day": data["date"].day
                },
                status=data["status"]
            )

            return render(
                request,
                "event_created.html",
                {
                    "event": event
                }
            )

def event_edit(request, event_id):
    if request.method == "POST":
        form = forms.EditEventForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            event = edit_event(
                user_id=request.user.id,
                event_id=event_id,
                title=data["title"],
                description=data["description"],
                status=data["status"]
            )

            return render(
                request,
                "event_edited.html",
                {
                    "event": event
                }
            )