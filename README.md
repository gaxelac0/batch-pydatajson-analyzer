# batch-pydatajson-analyzer
Little python script to analyze metadata of Argentine data.json site-nodes. 

# Execute
python metadata.py --file ./test/samples/nodes.csv

# Result
Output file: ./test/result/result.csv


![alt text](https://github.com/gaxelac0/batch-pydatajson-analyzer/blob/main/res/static-csv.png?raw=true)
Se puede abrir el csv con buen formato en excel siguiendo esta guía
https://www.exceldemy.com/open-csv-file-in-excel-with-columns-automatically/

TODO list: 
- /home/ubu-dev-env/development/repos/batch-pydatajson-analyzer/output.py:144: FutureWarning: Behavior when concatenating bool-dtype and numeric-dtype arrays is deprecated; in a future version these will cast to object dtype (instead of coercing bools to numeric values). To retain the old behavior, explicitly cast bool-dtype arrays to numeric dtype. curr_dataframe = pd.concat([curr_dataframe, append_dataframe], axis=0)
/home/ubu-dev-env/development/repos/batch-pydatajson-analyzer/output.py:93: FutureWarning: Behavior when concatenating bool-dtype and numeric-dtype arrays is deprecated; in a future version these will cast to object dtype (instead of coercing bools to numeric values). To retain the old behavior, explicitly cast bool-dtype arrays to numeric dtype. return pd.concat([curr_dataframe, append_dataframe], axis=0)
- clean unused imports
- better comment code
- there is an error in distribution types plot: not showing distribution types correctly.
- sometimes there is a discrepancy between the data type shown in some of the columns, e.g, Dataset Errors in catalog indicator shows TRUE or 1 sometimes.
- DCAT schema validation? test with Tigre data.json