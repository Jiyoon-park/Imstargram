from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.
class User(AbstractUser):
    # userimage = models.ImageField()
    # userimage_thumbnail = ImageSpecField(source='userimage',
    #                                   processors=[Thumbnail(100, 100)],
    #                                   format='JPEG',
    #                                   options={'quality': 60})
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings'
    )
