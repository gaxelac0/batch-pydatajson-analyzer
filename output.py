#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import date
import util, csv

dfc = 'distribuciones_formatos_cant'

def generate_distribution_types_pie_chart(stats_counter, qty):

    all = stats_counter.most_common(None)

    qty = len(all) if qty > len(all) else qty

    most_common = all[:qty]
    others = all[qty:]

    others_val = 0
    others_legend = []
    for tuple in others:
        others_legend.append(tuple[0])
        others_val += tuple[1]

    #others_tuple = (', '.join(others_legend), others_val)
    others_tuple = ('OTHERS', others_val)

    result_counter = most_common
    result_counter.append(others_tuple)

    labels = []
    for tuple in result_counter: 
        labels.append(tuple[0])

    values = []
    for tuple in result_counter: 
        values.append(tuple[1])

    explode = []
    for i in range(qty):
        explode.append(0)
    explode.append(0.3)

    fig = plt.figure(figsize=(10,7))
    plt.pie(values, labels = labels, autopct='%1.1f%%', pctdistance=1.1, labeldistance=1.2, explode=explode)

    others_patch = mpatches.Patch(color='gray', label="OTHERS: "+', '.join(others_legend))

    plt.legend(handles=[others_patch])

    plt.savefig('.//test//result//charts//distribution-types-pie-chart-'+str(qty)+'.png')

def generate_output_catalog_indicator(file, source, accessible, indicators=None, dist_type_counter=None):

    # runs once
    write_catalog_indicator_header(file)
   
    if indicators != None:
        indicators = indicators[0][0]

        dist_type_counter.update(indicators[dfc])
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