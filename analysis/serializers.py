from rest_framework import serializers
from .models import Product


class AnalysisSerializer(serializers.ModelSerializer):
    correlation = serializers.CharField(max_length=20)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'date_w', 'price', 'total_vol', 'plu1', 'plu2', 'plu3', 'bags_t', 'bags_s',
                  'bags_l', 'bags_lx', 'type', 'year', 'location')