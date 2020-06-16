from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    roles = {
        "admin": "Администратор",
        "active_user": "Активный пользователь",
        "simple_user": "Простой пользователь",
    }

    role = models.CharField(max_length=24, default="simple_user")
    rating = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    forum_nickname = models.CharField(max_length=75, default="user_nickname")
    bio = models.TextField(max_length=2048, blank=True)
    phone_number = models.CharField(max_length=15, null=True)
    phone_number_verify_code = models.CharField(max_length=4, null=True)

    photo = models.ImageField(upload_to="user_images", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        shop = self.shops.first()
        res = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.first_name + " " + self.last_name,
            "email": self.email,
            "bio": self.bio,
            "is_superuser": self.is_superuser,
            "rating": str(self.rating),
            "shop_name": shop.name if shop else '',
            "profile_link": f'http://127.0.0.1:8000/blogs/{self.id}/',
            "image_url": 'http://127.0.0.1:8000/static/' + self.photo.url if self.photo else 'https://banner2.cleanpng.com/20180401/kve/kisspng-user-'
                                                           'profile-computer-icons-male-id-5ac19772b4d884.'
                                                           '3909818215226366587408.jpg',
        }

        return res


class ActivityLog(models.Model):
    user = models.ForeignKey(User, related_name="user_log", related_query_name="activity_logs",
                             on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    visited_pages_count = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
