from django.forms import ModelForm
from emails.models import Content
from django import forms

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ["title", "coverImage", "description"]


    # customizing form fields such as classes, attributes, ids, etc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)