from django.db import models


class Product(models.Model):
    """
    Product model to store the product details
    """
    date_w = models.DateField()
    price = models.FloatField()
    total_vol = models.FloatField()
    plu1 = models.FloatField()
    plu2 = models.FloatField()
    plu3 = models.FloatField()
    bags_t = models.FloatField()
    bags_s = models.FloatField()
    bags_l = models.FloatField()
    bags_lx = models.FloatField()
    type = models.CharField(max_length=1)
    year = models.IntegerField()
    location = models.CharField(max_length=25)

    def __str__(self):
        return str(self.id) + " : " + self.location
