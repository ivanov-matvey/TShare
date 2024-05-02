from django.db import models
from django.contrib.auth.models import User


class Block(models.Model):
    LIFE_TIME = {
        '5': '5 minutes',
        '10': '10 minutes',
        '30': '30 minutes',
        '60': '1 hour',
        '1440': '24 hours'
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    delete_after = models.CharField(max_length=4, choices=LIFE_TIME, default='5')
    url = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.text[0:50]}'
