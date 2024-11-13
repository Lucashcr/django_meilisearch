"""
Admin dashboard configuration for the api app.
"""

from django.contrib import admin

from .models import Post

# Register your models here.
admin.site.register(Post)
