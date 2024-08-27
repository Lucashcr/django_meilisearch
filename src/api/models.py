from django.db import models


# Create your models here.
class Post(models.Model):
    title: models.CharField = models.CharField(max_length=100)
    content: models.TextField = models.TextField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Post({self.title} | {self.created_at.strftime("%Y-%m-%d %H:%M:%S")})'
