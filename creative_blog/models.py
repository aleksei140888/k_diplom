from django.db import models
from main_site.models import User


class MasterClass(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)

    author = models.ForeignKey(User, related_name="master_classes", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        photo = self.photo.first()
        video = self.video.first()

        return {
            'id': self.id,
            'title': self.title,
            'text': self.text[:500],
            'author': self.author.to_dict(),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'photo': photo.filename.url if photo else 'images/article_img.png',
            'video': video.filename.url if video else False,
        }

    def to_dict_full(self):
        photo = self.photo.first()
        video = self.video.first()

        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'author': self.author.to_dict(),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'photo': photo.filename.url if photo else 'images/article_img.png',
            'video': video.filename.url if video else False,
        }


class MasterClassPhoto(models.Model):
    master_class = models.ForeignKey(MasterClass, related_name="photo", on_delete=models.CASCADE)
    filename = models.ImageField(upload_to='', blank=True)
    extension = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def file(self):
        return self.filename.url


class MasterClassVideo(models.Model):
    master_class = models.ForeignKey(MasterClass, related_name="video", on_delete=models.CASCADE)
    filename = models.FileField(upload_to='', blank=True)
    extension = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def file(self):
        return self.filename.url
