# -*- coding: utf-8 -*-
from django import template
from django.db.models import Count, Q
from django.utils.timezone import utc
from datetime import datetime
from produtos.models import CategoriaProduto, Produto
from utils.quick_tag import quick_tag

register = template.Library()

@register.tag('get_categorias')
@quick_tag
def get_categorias(context, limite=0):
	if limite == 0:
		context['categorias'] = CategoriaProduto.objects.all().order_by('nome')
	else:
		categorias = []
		iterator = CategoriaProduto.objects.iterator()
		i = 0
		for c in iterator:
			if i >= limite:
				break
			else:
				if not c.vazia():
					categorias.append(c.id)
					i += 1
		context['categorias'] = CategoriaProduto.objects.filter(id__in=categorias).order_by('nome')
	return ''

@register.tag('get_populares')
@quick_tag
def get_populares(context, limite=0):
	if not 'populares' in dir(context):
		try:
			populares = Produto.objects.all().annotate(n_pedidos=Count('itens_pedido')).order_by('-n_pedidos')
			if limite == 0:
				context['populares'] = populares
			else:
				if populares.count() < limite:
					context['populares'] = populares
				else:
					context['populares'] = populares[:limite]
		except:
			return ''
	return ''

@register.tag('get_ofertas')
@quick_tag
def get_ofertas(context, limite=0):
	if not 'ofertas' in dir(context):
		try:
			ofertas = Produto.objects.filter(preco_desconto__isnull=False)
			ofertas.filter(Q(limite_desconto__isnull=True) | Q(limite_desconto__gte=datetime.utcnow().replace(tzinfo=utc)))
			ofertas.order_by('-limite_desconto')
			if limite == 0:
				context['ofertas'] = ofertas
			else:
				if ofertas.count() < limite:
					context['ofertas'] = ofertas
				else:
					context['ofertas'] = ofertas[:limite]
		except:
			return ''
	return ''