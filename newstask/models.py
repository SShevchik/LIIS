from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    class AccessCategory(models.TextChoices):
        PUBLIC = 'PC', _('Public')
        AUTHORISED = 'AD', _('Authorised')
        SUBSCRIPTION = 'SN', _('Subscription')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(unique=True, max_length=100)
    content = models.TextField()
    access_category = models.CharField(max_length=2, choices=AccessCategory.choices, default=AccessCategory.PUBLIC)

    def get_absolute_url(self):
        return reverse('home')


class Subscription(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
