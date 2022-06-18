import csv
import json
from pydatajson import DataJson
from csv import reader
from csv import writer

import argparse

# parse arguments
parser = argparse.ArgumentParser(description='Test file')
parser.add_argument('--file', type=str, help='A required file to process.')
args = parser.parse_args()

dj = DataJson()
try:
    f = open('./test/result/result.csv', 'w')
    header = ['Catalog Link', 'Catalog Errors', 'Catalog Error Desc', 'Dataset title', 'Dataset Errors', 'Dataset Error Desc']
    writer = csv.writer(f)
    writer.writerow(header)
    # open file in read mode
    with open(args.file, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        catalogs = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for catalog in catalogs:
            catalog = catalog[0]
            print ('Catalog: ' + catalog + '\n')
            result = dj.is_valid_catalog(catalog)
            validation_report = dj.validate_catalog(catalog)
            print('Result: ' + str(result) + '\n')
            print('Report: ' + str(validation_report) + '\n')

            categories = validation_report['error']
            if result == True:
                for cat in categories: 
                    if cat == 'dataset' and categories[cat] != None:
                        for dataset in categories[cat]:
                            data = [catalog, False, 'None', dataset['title'], False, 'None']
                            writer = csv.writer(f)
                            writer.writerow(data)
            else:
                catalog_error = False
                catalog_error_desc = ''
                for cat in categories: 
                    if cat == 'catalog' and categories[cat] != None:
                        if categories[cat]['status'] != 'OK':
                            catalog_error = True
                            for cat_err in categories[cat]['errors']: 
                                catalog_error_desc = catalog_error_desc + cat_err['message'] +' && '
                    elif cat == 'dataset' and categories[cat] != None:
                        for dataset in categories[cat]:
                            if dataset['status'] == 'ERROR':
                                final_error_conc = ''
                                for error in dataset['errors']:
                                    final_error_conc  = final_error_conc + error['message'] + ' && '
                                data = [catalog, catalog_error, catalog_error_desc, dataset['title'], True, final_error_conc]
                                writer = csv.writer(f)
                                writer.writerow(data)
    f.close()
except Exception as e:
    print("error: {0}".format(e) + '\n')