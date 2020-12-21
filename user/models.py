from django.db import models

# Create your models here.
from django.forms import ModelForm
from house.models import House, Images


class HouseImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']



