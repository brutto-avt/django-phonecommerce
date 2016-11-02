# -*- coding: utf-8 -*-
from django import template
from utils.quick_tag import quick_tag
from utils.correios import calcula_frete_ws

register = template.Library()

@register.tag('calcula_frete')
@quick_tag
def calcula_frete(context):
	try:
		pedido = context['pedido']
		cep = context['user'].cliente.cep
		frete = calcula_frete_ws(cep, pedido)
		if isinstance(frete, unicode):
			context['erro'] = frete
		else:
			context['valor_frete'] = frete
	except:
		return ''
	return ''