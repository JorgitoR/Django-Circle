import random
import csv
from datetime import timedelta

from cride.circles.models.circles import Circle

#https://gist.github.com/pablotrinidad/93ee462e0ee761bd505f0a2fed3d1c8c

def load_circles(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)[1:]
        for row in rows:
            c = Circle.objects.create(
                name=row[0],
                slug_name=row[1],
                is_public=row[2] == '1',
                verified=row[3] == '1',
                is_limited=row[4] != '0',
                members_limit=0 if row[4] == '0' else int(row[4])
            )
            print(c)

load_circles('circless.csv')
