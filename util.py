import constants

def write_to_file(file_writer, dataframe, sheet_name):
    dataframe.to_excel(file_writer, sheet_name=sheet_name, index=False)