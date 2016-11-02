#-*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from produtos.models import CategoriaProduto, Produto
from pedidos.views import get_carrinho

@csrf_exempt
def busca(request):
	query = request.GET['q']
	carrinho = get_carrinho(request)
	if request.is_ajax():
		context = {}
		response = HttpResponse()
		msg = None
		more = False
		produtos = Produto.objects.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))
		if produtos.count() == 0:
			msg = 'Nenhum produto encontrado'
		elif produtos.count() > 5:
			more = True
			produtos = produtos[:5]
		html = render_to_string('componentes/includes/live-search.html', {
			'msg': msg,
			'more': more,
			'query': query,
			'produtos': produtos,
			'request': request
		})
		context = {'html': html}
		html = mark_safe(html.strip(u'\ufeff').strip())
		simplejson.dump(context, response)
		return response
	else:
		produtos = Produto.objects.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))
		if produtos.count() == 0:
			produtos = None
			msg = 'Nenhum produto encontrado'
		return render_to_response('produtos/busca.html', locals(), context_instance=RequestContext(request))

def categorias(request):
	carrinho = get_carrinho(request)
	categorias = CategoriaProduto.objects.all()
	return render_to_response('produtos/lista_categorias.html', locals(), context_instance=RequestContext(request))
	
def categorias_produto(request, slug_categoria):
	carrinho = get_carrinho(request)
	categoria = get_object_or_404(CategoriaProduto, slug=slug_categoria)
	categorias = categoria.filhos.filter()
	return render_to_response('produtos/lista_categorias.html', locals(), context_instance=RequestContext(request))
	
def produtos(request, slug_categoria):
	carrinho = get_carrinho(request)
	categoria = get_object_or_404(CategoriaProduto, slug=slug_categoria)
	produtos = Produto.objects.filter(categoria=categoria)
	return render_to_response('produtos/lista_produtos.html', locals(), context_instance=RequestContext(request))
	
def detalhe_produto(request, slug_categoria, slug):
	carrinho = get_carrinho(request)
	produto = get_object_or_404(Produto, slug=slug)
	return render_to_response('produtos/produto.html', locals(), context_instance=RequestContext(request))