#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import date
import util, csv
import pandas as pd
import constants

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

    #plt.savefig('.//test//result//charts//distribution-types-pie-chart-'+str(qty)+'.png')

def generate_output_catalog_indicator(curr_dataframe, source, accessible, indicators=None, dist_type_counter=None):

    if not isinstance(curr_dataframe, pd.DataFrame) and curr_dataframe == None:
        curr_dataframe = write_catalog_indicator_header()
   
    if indicators != None:
        indicators = indicators[0][0]

        # actualizamos el contador de estadisticas de tipos de distribucion 
        dist_type_counter.update(indicators[dfc])

        append_dataframe = pd.DataFrame({
            'Origen/URL': [source],
            'Accessible ('+ date.today().strftime("%d/%m/%Y") +')': [accessible],
            'Titulo': [accessible],
            'Actualizado hace (dias)': [indicators['title']],
            'Cantidad Dataset': [indicators['catalogo_ultima_actualizacion_dias']],
            'JSON': [indicators['datasets_cant']],
            'PDF': [indicators['datasets_meta_error_cant']],
            'XLS': [indicators[dfc]['JSON'] if 'JSON' in indicators[dfc] else 0],
            'CSV': [indicators[dfc]['PDF'] if 'PDF' in indicators[dfc] else 0],
            'JPG': [indicators[dfc]['JPG'] if 'JPG' in indicators[dfc] else 0],
            'XML': [indicators[dfc]['XML'] if 'XML' in indicators[dfc] else 0],
            'DOC': [indicators[dfc]['DOC'] if 'DOC' in indicators[dfc] else 0],
            'PPT': [indicators[dfc]['PPT'] if 'PPT' in indicators[dfc] else 0],
        })
    return pd.concat([curr_dataframe, append_dataframe], axis=0)


def generate_output_per_dataset(curr_dataframe, source, result, validation_report):

    if not isinstance(curr_dataframe, pd.DataFrame) and curr_dataframe == None:
        curr_dataframe = write_per_dataset_header()

    categories = validation_report['error']
    if result == True:
        for cat in categories: 
            if cat == 'dataset' and categories[cat] != None:
                for dataset in categories[cat]:

                    append_dataframe = pd.DataFrame({ 
                        'URL': [source],
                        'Catalog Errors': [False],
                        'Catalog Error Desc': ['None'],
                        'Dataset title': dataset['title'],
                        'Dataset Errors': [False],
                        'Dataset Error Desc': ['None'],
                    })


                    curr_dataframe = pd.concat([curr_dataframe, append_dataframe], axis=0)
                    #util.write_to_file(file_writer, dataframe=dataframe, sheet_name=constants.DATASET_REPORT_SHEET_NAME)
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
                       
                        append_dataframe = pd.DataFrame({ 
                            'URL': [source],
                            'Catalog Errors': [catalog_error],
                            'Catalog Error Desc': [catalog_error_desc],
                            'Dataset title': dataset['title'],
                            'Dataset Errors': [True],
                            'Dataset Error Desc': [final_error_conc],
                        })
                        
                        curr_dataframe = pd.concat([curr_dataframe, append_dataframe], axis=0)
                       #util.write_to_file(file_writer, dataframe, constants.DATASET_REPORT_SHEET_NAME)
    return curr_dataframe

def write_per_dataset_header():

    # Header Dataframe
    header_df = pd.DataFrame({
         'URL': [],
         'Catalog Errors': [],
         'Catalog Error Desc': [],
         'Dataset title': [],
         'Dataset Errors': [],
         'Dataset Error Desc': [],
    })
    return header_df

def write_catalog_indicator_header():

    header_df = pd.DataFrame({ 
        'Origen/URL': [],
        'Accessible ('+ date.today().strftime("%d/%m/%Y") +')': [],
        'Titulo': [],
        'Actualizado hace (dias)': [],
        'Cantidad Dataset': [],
        'JSON': [],
        'PDF': [],
        'XLS': [],
        'CSV': [],
        'JPG': [],
        'XML': [],
        'DOC': [],
        'PPT': [],
    })
    return header_df