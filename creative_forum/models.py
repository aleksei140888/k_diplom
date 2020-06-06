from django.db import models
from main_site.models import User


class Topic(models.Model):
    topic_status_list = [
        'opened',
        'closed',
    ]

    topic_creator = models.ForeignKey(User, related_name="creator", related_query_name="topics", on_delete=models.CASCADE )
    status = models.CharField(max_length=20, default="opened")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class TopicAnswer(models.Model):
    answer_creator = models.ForeignKey(User, related_name="+", related_query_name="answers", on_delete=models.CASCADE)
    answer_for_topic = models.ForeignKey(Topic, related_name="topic", related_query_name="answers", on_delete=models.CASCADE)
    text = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


