from django.db import models

class ChatIds(models.Model):
    caffeName = models.CharField(max_length=500)
    chatId = models.CharField(max_length=500)





