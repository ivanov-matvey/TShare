from django.forms import ModelForm
from .models import Block


class BlockForm(ModelForm):
    class Meta:
        model = Block
        fields = '__all__'
        exclude = ['user', 'url', 'created', 'updated']
        help_texts = {
            'username': None,
            'email': None,
        }
