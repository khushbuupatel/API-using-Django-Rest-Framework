from django.contrib import admin
from .models import Product

# register the Product model with the admin site
admin.site.register(Product)
