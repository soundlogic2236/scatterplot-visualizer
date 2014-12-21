import random
import csv
with open('points.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)

    row = []
    for i in range(1000):
        row.append(random.randrange(-2000,1000))
        row.append(random.randrange(20,1000))
        row.append(random.randrange(0,3))
        writer.writerow(row)
        row = []
