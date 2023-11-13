from django.forms import ModelForm
from django import forms
from .models import Pos



class CreatePosForm(ModelForm):
    class Meta:
        model = Pos
        fields = ('pos_name',)


class EditPosForm(ModelForm):
    class Meta:
        model = Pos
        fields = ('pos_name',)