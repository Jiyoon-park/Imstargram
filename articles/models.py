from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail

# Create your models here.
class Article(models.Model):
    image = models.ImageField()
    #db 저장이 아니라, 마이그레이션 안해도 되는 것.
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[Thumbnail(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})
    # image_thumbnail = ProcessedImageField(upload_to='image',
    #                                       processors=[Thumbnail(300, 300)],
    #                                       format='JPEG',
    #                                       options={'quality': 60})
    content = models.TextField()
    location = models.CharField(max_length=20)
    withsomeone = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_articles'
    )

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)