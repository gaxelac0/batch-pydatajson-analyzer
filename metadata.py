import csv, random, time, json, util, requests, output
from email import header
from typing import Counter
import stats
from pydatajson import DataJson, readers, writers
from csv import reader, writer

import constants

import pandas as pd


import argparse

# parse arguments
parser = argparse.ArgumentParser(description='Test file')

required = parser.add_argument_group('argumentos obligatorios')
optional = parser.add_argument_group('argumentos opcionales')
required.add_argument('--f', required=True, type=str, help='Argumento obligatorio que lista los nodos a procesar, ej: http://datos.gob.ar/data.json')
optional.add_argument('--p', type=str, help='Argumento opcional que indica que se desea agregar un prefijo al nombre de los archivos de salida, \
                                                ej: yerbabuena para generar archivos de salida yerbabuena-catalog-indicators.csv y yerbabuena-result-per-dataset.csv.')
optional.add_argument('--d', type=bool, help='Argumento opcional que indica que se desea que se descargue el archivo data.json al disco duro.')


optional.add_argument('--q', type=int, default=4, help='Argumento opcional que indica la cantidad de tipos de distribuciones a mostrar en los pie charts. \
Por defecto muestra las 4 mas presentes y agrupa las demas en "Otros".')
args = parser.parse_args()

datajson = DataJson()

preffix = args.p + '-' if args.p != None else ''

workbook_filename = './test/result/' + preffix + 'result.xlsx'

result_writer = pd.ExcelWriter(workbook_filename, engine='xlsxwriter')

# Contador para los tipos de distribucion para luego armar el pie chart
dist_type_counter = Counter()

# Dataframes utilizados para ir concatenando los resultados linea a linea
result_per_dataset_df, result_catalog_indicator_df = None, None

# se itera una a una las lineas del archivo de entrada
with open(args.f, 'r') as read_obj:
    sources = reader(read_obj)
    for source in sources:

        # por cada una de ellas se determina si es accesible o no, los archivos locales siempre son accesibles
        accessible = False
        source = source[0]
        print('\n' + 'reading catalog: ' + source + '\n')

        # se chequea si es un link remoto o archivo local
        # if "http" in source:
        #     try:
        #         r = requests.get(source, timeout=3)
        #         if r.status_code == 200:
        #             accessible = True
        #     except requests.exceptions.Timeout as e:
        #         print("error: {0}".format(e) + '\n')
        # else:
        #     accessible = True

        indicators = None
        if not accessible:

            # Lee el catalogo, el origen puede ser un archivo local, url remota. Se aceptan XSLX, JSON
            catalog_dict = None
            try:
                catalog_dict = readers.read_catalog(source)
            except:
                continue

             # en caso de un catalogo pesado, para exportarlo a un archivo local
            if args.d:
                export_name =str(random.sample(range(100000, 999999), 1)[0])+".data.json"
                path = "test/samples/" + export_name
                print('Descargando copia local en ' + path)
                writers.write_json(obj=catalog_dict,path=path)
                
            # Valida el catalogo
            result = datajson.is_valid_catalog(catalog_dict)
            # Generacion de reporte de la validacion
            validation_report = datajson.validate_catalog(catalog_dict)
            # Generacion de indicadores 
            indicators = datajson.generate_catalogs_indicators(catalog_dict)
            print('Catalogo valido: ' + str(result) + '\n')
            #print('Report: ' + str(validation_report) + '\n')

            # se concatena el reporte por dataset calculado al dataframe de salida
            result_per_dataset_df = output.generate_output_per_dataset(result_per_dataset_df, source, result, validation_report)

        # se concatena el reporte de catalogo calculado al dataframe de salida
        result_catalog_indicator_df = output.generate_output_catalog_indicator(result_catalog_indicator_df, source, accessible, indicators, dist_type_counter)




util.write_to_file(result_writer, dataframe=result_per_dataset_df, sheet_name=constants.DATASET_REPORT_SHEET_NAME)
util.write_to_file(result_writer, dataframe=result_catalog_indicator_df, sheet_name=constants.CATALOG_REPORT_SHEET_NAME)

result_writer.close()

# generacion del pie chart de tipos de distribucion
output.generate_distribution_types_pie_chart(dist_type_counter, args.q, workbook_filename)


#result_catalog_indicator.close()

