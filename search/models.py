from django.db import models
from django.contrib.auth import get_user_model
from categories.models import Category  # Replace `your_app_name` with the app where the `Category` model is defined.

User = get_user_model()

class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searches')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='searches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Search by {self.user.username} in category {self.category.name}"
