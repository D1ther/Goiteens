from . import models
from django.forms import ModelForm

class CreateEventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = ["title", "description", "date", "status"]

class EditEventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = ["title", "description", "status"]