import csv, random, time, json, util, requests, output
from pydatajson import DataJson, readers, writers
from csv import reader, writer


import argparse

# parse arguments
parser = argparse.ArgumentParser(description='Test file')
parser.add_argument('--file', type=str, help='A required with listed nodes file to process.')
args = parser.parse_args()

datajson = DataJson()

result_per_dataset = open('./test/result/result-per-dataset.csv', 'w', newline='')

header = ['URL', 'Catalog Errors', 'Catalog Error Desc', 'Dataset title', 'Dataset Errors', 'Dataset Error Desc']
util.write_to_file(result_per_dataset, header)

# se itera una a una las lineas del archivo de entrada
with open(args.file, 'r') as read_obj:
    sources = reader(read_obj)
    for source in sources:

        # por cada una de ellas se determina si es accesible o no, los archivos locales siempre son accesibles
        accessible = False
        source = source[0]
        print('\n' + 'reading catalog: ' + source + '\n')

        # se chequea si es un link remoto o archivo local
        if "http" in source:
            try:
                r = requests.get(source, timeout=3)
                if r.status_code == 200:
                    accessible = True
            except requests.exceptions.Timeout as e:
                print("error: {0}".format(e) + '\n')
        else:
            accessible = True

        # en caso de un catalogo pesado, para exportarlo a un archivo local
        # export_name =str(random.sample(range(100000, 999999), 1)[0])+".data.json"
        # path = "test/samples/"+export_name
        # print(path)
        # catalog_dict = readers.read_catalog(source)
        # writers.write_json(obj=catalog_dict,path=path)

        indicators = None
        if accessible:

            # Lee el catalogo, el origen puede ser un archivo local, url remota. Se aceptan XSLX, JSON
            catalog_dict = readers.read_catalog(source)
            # Valida el catalogo
            result = datajson.is_valid_catalog(catalog_dict)
            # Generacion de reporte de la validacion
            validation_report = datajson.validate_catalog(catalog_dict)
            # Generacion de indicadores 
            indicators = datajson.generate_catalogs_indicators(catalog_dict)
            print('Catalogo valido: ' + str(result) + '\n')
            #print('Report: ' + str(validation_report) + '\n')

            # se genera archivo de salida por dataset
            output.generate_output_per_dataset(result_per_dataset, source, result, validation_report)

     # se genera archivo de salida de indicadores de catalogo
    output.generate_output_catalog_indicator(source, accessible, indicators)

result_per_dataset.close()



