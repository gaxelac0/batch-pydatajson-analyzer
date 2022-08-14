from datetime import date
import util, csv

header = None
dfc = 'distribuciones_formatos_cant'

def generate_output_catalog_indicator(file, source, accessible, indicators=None):

    # runs once
    write_catalog_indicator_header(file)
   
    if indicators != None:
        indicators = indicators[0][0]
        data = [source, False, accessible, indicators['title'],
                indicators['catalogo_ultima_actualizacion_dias'],
                indicators['datasets_cant'],
                indicators['datasets_meta_error_cant'],
                indicators[dfc]['JSON'] if 'JSON' in indicators[dfc] else 0,
                indicators[dfc]['PDF'] if 'PDF' in indicators[dfc] else 0,
                indicators[dfc]['XLS'] if 'XLS' in indicators[dfc] else 0,
                indicators[dfc]['CSV'] if 'CSV' in indicators[dfc] else 0,
                indicators[dfc]['JPG'] if 'JPG' in indicators[dfc] else 0,
                indicators[dfc]['XML'] if 'XML' in indicators[dfc] else 0,
                indicators[dfc]['DOC'] if 'DOC' in indicators[dfc] else 0,
                indicators[dfc]['PPT'] if 'PPT' in indicators[dfc] else 0]
        util.write_to_file(file, data)

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

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def write_catalog_indicator_header(file):
    header = ['Origen/URL', 'Accessible ('+ date.today().strftime("%d/%m/%Y") +')', 'Titulo', 'Actualizado hace (dias)', 'Cantidad Dataset', 'Errores Dataset', 'JSON', 'PDF', 'XLS', 'CSV', 'JPG', 'XML', 'DOC', 'PPT']
    util.write_to_file(file, header)