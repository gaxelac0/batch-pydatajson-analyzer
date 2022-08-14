import util, csv

def generate_output_catalog_indicator(source, accessible, indicators=None):

    file = open('./test/result/catalog-indicators.csv', 'w', newline='')
    header = ['Origen/URL', 'Accesible?', 'Titulo', 'Actualizado hace (dias)']
    util.write_to_file(file, header)
   
    if indicators != None:
        indicators = indicators[0][0]
        data = [source, False, accessible, indicators['title'], indicators['catalogo_ultima_actualizacion_dias'] ]
        util.write_to_file(file, data)

    file.close()

def generate_output_per_dataset(file, source, result, validation_report):
    categories = validation_report['error']
    if result == True:
        for cat in categories: 
            if cat == 'dataset' and categories[cat] != None:
                for dataset in categories[cat]:
                    data = [source, False, 'None', dataset['title'], False, 'None']
                    util.write_to_file(file, data)
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
                        data = [source, catalog_error, catalog_error_desc, dataset['title'], True, final_error_conc]
                        util.write_to_file(file, data)