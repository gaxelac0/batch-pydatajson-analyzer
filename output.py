import matplotlib.pyplot as plt
from datetime import date
import util, csv

dfc = 'distribuciones_formatos_cant'

dist_types = ['JSON', 'PDF', 'XLS', 'CSV', 'JPG', 'XML', 'DOC', 'PPT']


def generate_output_plot_indicator(stats_counter):

    x,y = zip(*stats_counter.most_common())
    print(x)
    print(y)

    plt.bar(x,y)
    plt.show()

def generate_output_catalog_indicator(file, source, accessible, indicators=None, stats_counter=None):

    # runs once
    write_catalog_indicator_header(file)
   
    if indicators != None:
        indicators = indicators[0][0]

        stats_counter.update(distribuciones_cant=indicators['distribuciones_cant'])
        stats_counter.update(indicators[dfc])

        # Cantidad de distribuciones por tipo
        pdf_qty = indicators[dfc]['PDF'] if 'PDF' in indicators[dfc] else 0
        json_qty = indicators[dfc]['JSON'] if 'JSON' in indicators[dfc] else 0,
        xls_qty = indicators[dfc]['XLS'] if 'XLS' in indicators[dfc] else 0,
        csv_qty = indicators[dfc]['CSV'] if 'CSV' in indicators[dfc] else 0,
        jpg_qty = indicators[dfc]['JPG'] if 'JPG' in indicators[dfc] else 0,
        xml_qty = indicators[dfc]['XML'] if 'XML' in indicators[dfc] else 0,
        doc_qty = indicators[dfc]['DOC'] if 'DOC' in indicators[dfc] else 0,
        ppt_qty = indicators[dfc]['PPT'] if 'PPT' in indicators[dfc] else 0

        # Actualizamos el objeto de stadisticas 
        # statistics.set_dist_qty(indicators['distribuciones_cant'])
        # statistics.set_pdf_qty(pdf_qty)
        # statistics.set_json_qty(json_qty)
        # statistics.set_xls_qty(xls_qty)
        # statistics.set_csv_qty(csv_qty)
        # statistics.set_jpg_qty(jpg_qty)
        # statistics.set_xml_qty(xml_qty)
        # statistics.set_doc_qty(doc_qty)
        # statistics.set_ppt_qty(ppt_qty)

        data = [source, False, accessible, indicators['title'],
                indicators['catalogo_ultima_actualizacion_dias'],
                indicators['datasets_cant'],
                indicators['datasets_meta_error_cant'],
                json_qty, pdf_qty, xls_qty, csv_qty,
                jpg_qty, xml_qty, doc_qty, ppt_qty]
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