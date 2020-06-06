from django.contrib import admin

# Register your models here.
from creative_shop.models import Shop, \
    Product, ProductCategory, DeliveryMethod, \
    ActiveDeliveryMethods, Card, CardItem, CardStatus
from main_site.models import User, ActivityLog
from creative_forum.models import TopicAnswer, Topic

admin.site.register(User)
admin.site.register(ActivityLog)


admin.site.register(Topic)
admin.site.register(TopicAnswer)

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(DeliveryMethod)
admin.site.register(ActiveDeliveryMethods)
admin.site.register(Card)
admin.site.register(CardItem)
admin.site.register(CardStatus)

