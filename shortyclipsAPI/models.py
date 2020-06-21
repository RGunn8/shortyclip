from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

from shortyclips import settings


class ClipUser(AbstractBaseUser):
    username = models.CharField(blank=False, unique=True, max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    password = models.CharField(blank=False, max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class Clip(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False)
    duration = models.IntegerField(default=0, blank=False)
    clipURL = models.URLField()
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    user = models.ForeignKey(to=ClipUser, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.OneToOneField(ClipUser, on_delete=models.CASCADE)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
