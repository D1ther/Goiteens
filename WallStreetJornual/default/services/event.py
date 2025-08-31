from .. import models

from django.shortcuts import get_object_or_404

import datetime
from typing import Dict


def get_events(username: str):
    user = get_object_or_404(models.User, username=username)

    if user.status == "ADMIN":
        return models.Event.objects.all()

    return models.Event.objects.filter(status="published")

def create_event(title: str, description: str, date: Dict[str, int], status: str = "draft"):
    today = datetime.date.today()

    current_date = datetime.date(date["year"], date["month"], date["day"])

    difference_date = current_date - today

    if difference_date.days <= 3:
        prioruty = "high"
    elif 3 < difference_date.days <= 7:
        prioruty = "medium"
    else:
        prioruty = "low"

    event = models.Event(
        title=title,
        description=description,
        date=current_date,
        priority=prioruty,
        status=status
    )

    event.save()

    return event

def edit_event(user_id: int, event_id: int, title: str, description: str, status: str):
    edited_user = get_object_or_404(models.User, id=user_id)
    event = get_object_or_404(models.Event, id=event_id)

    user = event.user

    if event.status not in "published":
        raise ValueError("Event cannot be edited")
    
    if edited_user.status != "admin" or edited_user != user:
        raise PermissionError("You do not have permission to edit this event")
    
    event.title = title
    event.description = description
    event.status = status
    event.save()

    return event