from trytond.pool import Pool
import datetime
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_DOWN
import tempfile

def header_a(invoice):   
	
	address = invoice.party.address_get()
	ret = dict(
		apellidoynombre = invoice.party.name,
		condiciones = invoice.payment_term.name,
		cuit_cliente = invoice.party.vat_number,
		nrofactura = invoice.number,
		fecha = invoice.invoice_date,
		nro_remito = '', #no esta el nro de remito en la factura??
		iva=(invoice.party and invoice.party.get_iva_condition()) or "",
		legajo7 = address.street + ' ' + address.city
	)
	return ret

def header_b(invoice):   
	
	address = invoice.party.address_get()
	ret = dict(
		apellidoynombre = invoice.party.name,
		condiciones = invoice.payment_term.name,
		cuit_cliente = invoice.party.vat_number,
		nrofactura = invoice.number,
		fecha = invoice.invoice_date,
		nro_remito = '', #no esta el nro de remito en la factura??
		iva=(invoice.party and invoice.party.get_iva_condition()) or "",
		legajo7 = address.street + ' ' + address.city
	)
	return ret

def detalle_a(invoice):

	#import pudb;pu.db
	def get_lineas(invoice):
		"""
		Retornamos una lista con las lineas de factura del tipo 'tipo'. La lista tiene
		tuplas: (nombre product, precio unitario, cantidad, importe de la linea)
		"""
		ret = []
		for line in invoice.lines:
			if line.type == 'line':            
				unit_price = Decimal(line.unit_price).quantize(Decimal(".01"), rounding=ROUND_DOWN)
				amount = Decimal(line.amount).quantize(Decimal(".01"), rounding=ROUND_DOWN)
				if len(line.description)>0:
					ret.append((line.description, unit_price, int(line.quantity), amount))
				else:
					ret.append((line.product.name, unit_price, int(line.quantity), amount))
		return ret

   
	lineas = get_lineas(invoice)
	
	return {
		"tabladetalle": lineas,
	}

def detalle_b(invoice):
	#import pudb;pu.db

	def get_lineas(invoice):
		"""
		Retornamos una lista con las lineas de factura del tipo 'tipo'. La lista tiene
		tuplas: (nombre product, precio unitario, cantidad, importe de la linea)
		"""
		ret = []
		for line in invoice.lines:
			if line.type == 'line':            
				unit_price = Decimal(line.unit_price).quantize(Decimal(".01"), rounding=ROUND_DOWN)
				amount = Decimal(line.amount).quantize(Decimal(".01"), rounding=ROUND_DOWN)
				
		if len(line.description)>0:
			ret.append((line.description, unit_price, int(line.quantity), amount))
		else:
			ret.append((line.product.name, unit_price, int(line.quantity), amount))
		return ret

   
	lineas = get_lineas(invoice)
	
	return {
		"tabladetalle": lineas,
	}



def footer_a(invoice):
	
	def get_total_factura(invoice):
		return round(invoice.total_amount,2)
	

	def get_codigo_qr():
		"""
		Escribimos el buffer de la imagen del codigo del QR
		en un tempfile para que lo use el template de la factura.
		"""
		if invoice.qr_imagen:
			temp_file = tempfile.NamedTemporaryFile(delete=False)
			temp_file.write(invoice.qr_imagen)
			temp_file.close()
			return temp_file.name
		return ""

	subtotal = get_total_factura(invoice)

	ret = dict(
		porciva = '21',
		subtotalgravado = '', #que es esto
		subtotalexento = '',  #que es esto
		subtotal = float(subtotal) - float(invoice.tax_amount),
		subtotaliva = invoice.tax_amount,
		total = subtotal,
		cae = 'CAE Nro: ' + str(invoice.pyafipws_cae),
		vencecae = 'Vto.de CAE: ' + str(invoice.pyafipws_cae_due_date.strftime("%d/%m/%Y")),
		codigo_qr = get_codigo_qr()
	)
	return ret

def footer_b(invoice):
	
	def get_total_factura(invoice):
		return round(invoice.total_amount,2)

	def get_codigo_qr():
		"""
		Escribimos el buffer de la imagen del codigo del QR
		en un tempfile para que lo use el template de la factura.
		"""
		if invoice.qr_imagen:
			temp_file = tempfile.NamedTemporaryFile(delete=False)
			temp_file.write(invoice.qr_imagen)
			temp_file.close()
			return temp_file.name
		return ""

	subtotal = get_total_factura(invoice)

	ret = dict(
		total = subtotal,
		cae = 'CAE Nro: ' + str(invoice.pyafipws_cae),
		vencecae = 'Vto.de CAE: ' + str(invoice.pyafipws_cae_due_date.strftime("%d/%m/%Y")),
		codigo_qr = get_codigo_qr()
	)
	return ret

SECCIONES_A = [
		header_a,
		detalle_a,
		footer_a
]

SECCIONES_B = [
		header_b,
		detalle_b,
		footer_b
]

def crear_data_factura_a(invoice):
	data = []
	for seccion in SECCIONES_A:
		data.append(seccion(invoice))
	return data

def crear_data_factura_b(invoice):
	data = []
	for seccion in SECCIONES_B:
		data.append(seccion(invoice))
	return data

def crear_data_nota_credito_a(invoice):
	data = []
	for seccion in SECCIONES_A:
		data.append(seccion(invoice))
	return data

def crear_data_nota_credito_b(invoice):
	data = []
	for seccion in SECCIONES_B:
		data.append(seccion(invoice))
	return data

def crear_data_nota_debito_a(invoice):
	data = []
	for seccion in SECCIONES_A:
		data.append(seccion(invoice))
	return data

def crear_data_nota_debito_b(invoice):
	data = []
	for seccion in SECCIONES_B:
		data.append(seccion(invoice))
	return data