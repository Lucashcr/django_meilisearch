"""
Models definition for the api app.
"""

from django.db import models


# Create your models here.
class Post(models.Model):
    """
    A model representing a blog post.

    Attributes:
        title (models.CharField): The post title.
        content (models.TextField): The post content.
        created_at (models.DateTimeField): The post creation date and time.
    """

    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Post({self.title} | {self.created_at.strftime("%Y-%m-%d %H:%M:%S")})'
