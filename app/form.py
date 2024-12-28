from django.db import models
from django import forms
from django.forms import fields
from.models import Applications, Students, SourceTable



class Userimage(forms.ModelForm):
    class Meta:
        model = Applications
        fields=('passport',)

class Userimage2(forms.ModelForm):
    class Meta:
        model = Students
        fields=('passport',)

class SourceTableForm(forms.ModelForm):
    session = forms.ChoiceField(choices=SourceTable.lv, required=False,label="Filter by session")
    class Meta:
        model = SourceTable
        fields= ('name','session','score')