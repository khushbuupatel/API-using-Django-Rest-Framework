import csv
import os
from datetime import datetime
from django_api import settings
from scripts import django_setup

# path of the csv file to be imported
csv_path = os.path.join(settings.BASE_DIR, 'product_a.csv')

# import the Product model after the django setup is done
from analysis.models import Product

with open(csv_path) as csv_file:
    # read the csv file
    reader = csv.DictReader(csv_file)

    # delete the objects previously present in the Product model
    Product.objects.all().delete()

    rowNo = 0
    for row in reader:
        # convert the date string into Datetime
        date = datetime.strptime(row['date_w'], "%Y-%m-%d")

        # create an object of Product model by entering all the details
        p = Product(date_w=date, price=float(row['price']), total_vol=float(row['total_vol']),
                    plu1=float(row['plu1']), plu2=float(row['plu2']),
                    plu3=float(row['plu3']), bags_t=float(row['bags_t']), bags_s=float(row['bags_s']),
                    bags_l=float(row['bags_l']),
                    bags_lx=float(row['bags_lx']), type=row['type'], year=int(row['year']), location=row['location'])

        # save the object into the model
        p.save()

        print("Row:", rowNo)
        rowNo = rowNo + 1
