import csv
number = input()
s = 0
with open('pirate_accounting.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, row in enumerate(reader):
        f = row[2].replace('x', '*')
        c = 0
        for i in f:
            if i != '*':
                c = 1
        if c == 0:
            if int(row[1]) > 1765 and len(row[2]) < int(number):
                s += row[3]
print(s)
