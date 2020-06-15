from django.db import models
from django.db.models import Sum

from live_portal import settings
from live_portal.utils import to_dict_list
from main_site.models import User


class Shop(models.Model):
    db_table = "shops"

    def __str__(self):
        return self.name

    rating = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    name = models.CharField(max_length=255, default="Мой магазин")
    description = models.TextField(default="Описание моего прекрастного магазина")
    owner = models.ForeignKey(User, related_name="shops", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductCategory(models.Model):
    db_table = "shops_products_category"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=75)


class Product(models.Model):
    db_table = "shops_products"

    def __str__(self):
        return self.name

    rating = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    shop = models.ForeignKey(Shop, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, related_name="products", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, default="Название товара", blank=True)
    description = models.TextField(default="Описание товара", blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)

    photo_filename = models.ImageField(upload_to='', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def get_photo_url(self):
        return self.photo_filename

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'rating_proc': int(self.rating / 5 * 100),
            'category': self.category.name if self.category else '',
            'description': self.description,
            'old_price': self.old_price,
            'new_price': self.new_price,
            'photo_filename': self.photo_filename.url,
        }


class DeliveryMethod(models.Model):
    db_table = "shops_delivery_methods"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, default="Метод доставки")
    slug = models.CharField(max_length=255, default="method")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    free_until = models.DateTimeField(auto_now_add=True)


class ActiveDeliveryMethods(models.Model):
    db_table = "shops_delivery_methods_active"

    shop = models.ForeignKey(Shop, related_name="active_delivery_methods",
                             on_delete=models.CASCADE)
    delivery_method = models.ForeignKey(DeliveryMethod, related_name="for_shop", on_delete=models.CASCADE)
    free_until = models.DateTimeField(auto_now_add=True)


class CardStatus(models.Model):
    db_table = "shops_card_statuses"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)


class Card(models.Model):
    db_table = "shops_cards"

    def __str__(self):
        return self.user.name

    user = models.ForeignKey(User, related_name="cards", on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name="cards", on_delete=models.CASCADE)
    status = models.ForeignKey(CardStatus, related_name="status", on_delete=models.CASCADE)
    delivery_method = models.ForeignKey(DeliveryMethod, related_name="delivery_method", on_delete=models.CASCADE, null=True)
    payed = models.BooleanField(default=0)
    order_id = models.CharField(max_length=255, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'shop': self.shop,
            'status': self.status,
            'products': to_dict_list(self.products.all()),
            'total_amount': self.get_amount(),
            'delivery_status': self.delivery_method.name if self.delivery_method else 'Не выбрано',
        }

    def get_amount(self):
        amount = 0

        for product in self.products.all():
            amount += product.item.new_price * product.count

        if self.delivery_method:
            amount += self.delivery_method.price
        return amount


class CardItem(models.Model):
    db_table = "shops_card_items"

    card = models.ForeignKey(Card, related_name="products", on_delete=models.CASCADE)
    item = models.ForeignKey(Product, related_name="products", on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def to_dict(self):
        return {
            'id': self.item.id,
            'name': self.item.name,
            'new_price': self.item.new_price,
            'full_price': self.item.new_price * self.count,
            'photo_filename': self.item.photo_filename,
            'category': self.item.category.name,
            'count': self.count,
        }
