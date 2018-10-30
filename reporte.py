from trytond.pool import Pool
from trytond.report import Report
import report_creator
from z3c.rml import rml2pdf
import template_fac_a, template_fac_b, template_nota_credito_a, template_nota_credito_b, template_nota_debito_a, template_nota_debito_b

class MyInvoiceReport(Report):
    __name__ = 'account.invoice'

    @classmethod
    def crear_reporte(cls, invoice):

        #import pudb;pu.db
        
        if invoice.invoice_type.invoice_type == '1': #Factura A
            datos = report_creator.crear_data_factura_a(invoice)
            rml_text = template_fac_a.get(*datos)
            out = rml2pdf.parseString(rml_text)
            return out.read()
        elif invoice.invoice_type.invoice_type == '6':  #Factura B
        #elif invoice.invoice_type.id == 18:  #Factura B
            datos = report_creator.crear_data_factura_b(invoice)
            rml_text = template_fac_b.get(*datos)
            out = rml2pdf.parseString(rml_text)
            return out.read()
        elif invoice.invoice_type.invoice_type == '3': #Nota de Credito A
            datos = report_creator.crear_data_nota_credito_a(invoice)
            rml_text = template_nota_credito_a.get(*datos)
            out = rml2pdf.parseString(rml_text)
            return out.read()
        elif invoice.invoice_type.invoice_type == '8':  #Nota de Credito B
            datos = report_creator.crear_data_nota_credito_b(invoice)
            rml_text = template_nota_credito_b.get(*datos)
            out = rml2pdf.parseString(rml_text)
            return out.read()
        elif invoice.invoice_type.invoice_type == '2':  #Nota de Debito A
            datos = report_creator.crear_data_nota_debito_a(invoice)
            rml_text = template_nota_debito_a.get(*datos)
            out = rml2pdf.parseString(rml_text)
            return out.read()
        elif invoice.invoice_type.invoice_type == '7':  #Nota de Debito B
            datos = report_creator.crear_data_nota_debito_b(invoice)
            rml_text = template_nota_debito_b.get(*datos)
            out = rml2pdf.parseString(rml_text)
            return out.read()



    @classmethod
    def parse(cls, report, records, data, localcontext):
        """
        Armamos los datos que vamos a mostrar en la factura.
        LLamamos a llenar el template.
        Transformamos el template en un pdf y lo retornamos.
        """
        invoice = records[0]
        repo = cls.crear_reporte(invoice)
        Invoice = Pool().get('account.invoice')
        Invoice.write([Invoice(invoice.id)], {
            'invoice_report_cache': repo})
        return ('pdf', repo)