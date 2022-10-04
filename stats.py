class Stats: 
    def __init__(self):
        # Cantidad total de distribuciones
        self.dist_qty = 0
        # Cantidad total de JSON
        self.json_qty = 0
        # Cantidad total de PDF
        self.pdf_qty = 0
        # Cantidad total de XLS
        self.xls_qty = 0
        # Cantidad total de CSV
        self.csv_qty = 0
        # Cantidad total de JPG
        self.jpg_qty = 0
        # Cantidad total de XML
        self.xml_qty = 0
        # Cantidad total de DOC
        self.doc_qty = 0
        # Cantidad total de PPT
        self.ppt_qty = 0

    def set_dist_qty(self, dist_qty):
        self.dist_qty = dist_qty

    def set_pdf_qty(self, pdf_qty):
        self.pdf_qty = pdf_qty[0] if type(pdf_qty) == tuple else pdf_qty

    def set_json_qty(self, json_qty):
        self.json_qty = json_qty[0] if type(json_qty) == tuple else json_qty

    def set_xls_qty(self, xls_qty):
        self.xls_qty = xls_qty[0] if type(xls_qty) == tuple else xls_qty

    def set_csv_qty(self, csv_qty):
        self.csv_qty = csv_qty[0] if type(csv_qty) == tuple else csv_qty

    def set_jpg_qty(self, jpg_qty):
        self.jpg_qty = jpg_qty[0] if type(jpg_qty) == tuple else jpg_qty

    def set_xml_qty(self, xml_qty):
        self.xml_qty = xml_qty[0] if type(xml_qty) == tuple else xml_qty

    def set_doc_qty(self, doc_qty):
        self.doc_qty = doc_qty[0] if type(doc_qty) == tuple else doc_qty

    def set_ppt_qty(self, ppt_qty):
        self.ppt_qty = ppt_qty[0] if type(ppt_qty) == tuple else ppt_qty