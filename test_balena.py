import csv

x = [1,1,1]
x = [x,x]

with open("testBalena.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(x)