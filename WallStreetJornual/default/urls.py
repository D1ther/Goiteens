from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.show_events, name="show_events"),
    path("events/add/", views.add_event, name="add_event"),
    path("events/<int:event_id>/edit/", views.edit_event, name="edit_event")
]