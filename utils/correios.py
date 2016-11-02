# -*- coding: utf-8 -*-
import httplib
import urllib
import re
from xml.dom.minidom import parse, parseString
from django.conf import settings

HOST = 'ws.correios.com.br'
URL_FRETE = '/calculador/CalcPrecoPrazo.aspx?'

def calcula_frete_ws(cep, pedido):
	frete = 0.0;
	
	for item in pedido.produtos.all():
		peso = '%.2f' % (item.produto.peso  * 3)
		largura = '%.2f' % (item.produto.altura + 5)
		altura = '%.2f' % item.produto.altura
		comprimento = '%.2f' % (item.produto.largura * 3)
		diametro = (float(altura) + float(largura)) * 2
		diametro = '%.2f' % diametro

		params = urllib.urlencode({
			'nCdEmpresa': '',
			'sDsSenha': '',
			'nCdServico': '41106',
			'sCepOrigem': settings.CEP_LOJA,
			'sCepDestino': cep.replace('-', ''),
			'nVlPeso': peso.replace('.',','),
			'nCdFormato': 1,
			'nVlComprimento': comprimento.replace('.',','),
			'nVlLargura': largura.replace('.',','),
			'nVlAltura': altura.replace('.',','),
			'nVlDiametro': diametro.replace('.',','),
			'sCdMaoPropria': 'N',
			'nVlValorDeclarado': 0.0,
			'sCdAvisoRecebimento': 'N',
			'StrRetorno': 'xml'
		})
		
		conn = httplib.HTTPConnection(HOST)
		conn.request('GET', URL_FRETE+params)
		response = conn.getresponse()
		dom = parseString( response.read() )
		conn.close()
	
		values = {'Valor':'', 'Erro':'', 'MsgErro': ''}
		for key in values.keys():
			try:
				values[key] = dom.getElementsByTagName(key)[0].childNodes[0].nodeValue
			except:
				pass

			
		if int(values['Erro']) != 0:
			return values['MsgErro']
		frete += float(values['Valor'].replace(',','.'))
	return frete