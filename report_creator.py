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

	porciva = ''
	porciva2 = ''
	porciva3 = ''
	subtotaliva = 0
	subtotaliva3 = 0
	subtotaliva2 = 0
	for tax_line in invoice.taxes:
		tax = tax_line.tax
		if tax.group.name == "IVA":
			if tax.rate == Decimal('0.21'):
				porciva = 'IVA 21.00'
				subtotaliva = subtotaliva + abs(tax_line.amount)
			elif tax.rate == Decimal('0.105'):
				porciva3 = 'IVA 10.50'
				subtotaliva3 = subtotaliva3 + abs(tax_line.amount)
			elif tax.rate == Decimal('0.025'):
				porciva2 = 'IVA  2.50'
				subtotaliva2 = subtotaliva2 + abs(tax_line.amount)
			else:
				pass

	if subtotaliva == 0:
		subtotaliva = ''
	if subtotaliva3 == 0:
		subtotaliva3 = ''
	if subtotaliva2 == 0:
		subtotaliva2 = ''


	ret = dict(
		subtotalgravado = '', #que es esto
		subtotalexento = '',  #que es esto
		subtotal = invoice.total_amount - invoice.tax_amount,
		total=invoice.total_amount,
		cae = 'CAE Nro: ' + str(invoice.pyafipws_cae),
		vencecae = 'Vto.de CAE: ' + str(invoice.pyafipws_cae_due_date.strftime("%d/%m/%Y")),
		codigo_qr = get_codigo_qr(),
		
		#esto lo agrego para poder tener dos tipos de alicuotas distintas
		porciva=porciva,
		subtotaliva=subtotaliva,
		porciva2=porciva2,
		subtotaliva2=subtotaliva2,
		porciva3=porciva3,
		subtotaliva3=subtotaliva3,

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