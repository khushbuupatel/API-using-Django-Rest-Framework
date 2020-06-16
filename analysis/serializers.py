from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'date', 'price', 'total_vol', 'plu1', 'plu2', 'plu3', 'bags_t', 'bags_s',
                  'bags_l', 'bags_lx', 'type', 'year', 'location')
