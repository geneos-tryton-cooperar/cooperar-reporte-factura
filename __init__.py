from trytond.pool import Pool
from .reporte import MyInvoiceReport

def register():
    Pool.register(
        MyInvoiceReport,
        module='cooperar-reporte-factura', type_='report')

