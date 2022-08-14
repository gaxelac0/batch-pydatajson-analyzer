
import csv

def write_to_file(f, data):
    writer = csv.writer(f)
    writer.writerow(data)