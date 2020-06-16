import csv
import os
from analysis.models import Product


def run():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_api.settings")
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'product_a.csv')

    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            p = Product(row[''], row['date'], row['price'], row['total_vol'], row['plu1'], row['plu2'], row['plu3'],
                        row['bags_t'], row['bags_l'], row['bags_lx'], row['type'], row['year'], row['location'])
            p.save()
