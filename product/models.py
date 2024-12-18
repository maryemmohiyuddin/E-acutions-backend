from django.db import models
from django.contrib.auth import get_user_model
from categories.models import Category

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=100)
    subName = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    yearOfManufacture = models.CharField(max_length=2000)
    width = models.CharField(max_length=2000)
    height = models.CharField(max_length=2000)
    weight = models.CharField(max_length=2000)
    Material = models.CharField(max_length=2000)
    picture = models.ImageField(upload_to='products/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # Adjust ID as needed

    def __str__(self):
        return self.name