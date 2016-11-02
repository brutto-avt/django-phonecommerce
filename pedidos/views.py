# -*-coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from produtos.models import Produto
from utils.pagseguro import Pagseguro
from utils.paypal import PayPal
from pedidos.carrinho import Carrinho
from pedidos.models import Carrinho as CarrinhoModel, ItemCarrinho
from pedidos.jqgrid import get_json, get_config

def get_carrinho(request):
	if request.user.is_authenticated():
		carrinho_id = request.session.get('carrinho_id')
		if carrinho_id:
			try:
				carrinho_model = CarrinhoModel.objects.get(id=carrinho_id, finalizado=False)
			except:
				carrinho_model = CarrinhoModel()
				carrinho_model.usuario = request.user
				carrinho_model.save()
				request.session['carrinho_id'] = carrinho_model.id
		else:
			carrinho_model = CarrinhoModel()
			carrinho_model.usuario = request.user
			carrinho_model.save()
			request.session['carrinho_id'] = carrinho_model.id
		carrinho = Carrinho(carrinho_model)
		return carrinho
	else:
		return None

@csrf_exempt
def carrinho_config(request):
	carrinho = get_carrinho(request).carrinho
	itens = ItemCarrinho.objects.filter(carrinho=carrinho)
	config = get_config(itens, 'carrinho_json', fields=['produto__nome', 'quantidade', 'produto__preco', 'valor_total'])
	return HttpResponse(config, mimetype="application/json")

@csrf_exempt
def carrinho_json(request):
	carrinho = get_carrinho(request).carrinho
	itens = ItemCarrinho.objects.filter(carrinho=carrinho)
	fields = ['produto__nome', 'quantidade', 'produto__preco', 'valor_total']
	json = get_json(request, itens, fields)
	return HttpResponse(json, mimetype="application/json")

@csrf_exempt
def carrinho(request):
	carrinho = get_carrinho(request)
	return render_to_response('pedidos/carrinho.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def adicionar_ao_carrinho(request, slug_produto):
	if not request.is_ajax():
		return HttpResponseForbidden('<h1>Permissão negada!</h1>')

	response = HttpResponse()
	produto = get_object_or_404(Produto, slug=slug_produto)
	quantidade = int(request.POST.get('quantidade', 1))
	carrinho = get_carrinho(request)
	if not produto.pode_vender(quantidade):
		context = {'msg':'N&atilde;o h&aacute; estoque suficiente para a quantidade pedida.', 'n_itens': carrinho.total_itens()}
		simplejson.dump(context, response)
		return response
	if request.method == 'POST':
		carrinho.adiciona_item(produto, quantidade)
	context = {'msg':'O item foi adicionado ao seu carrinho', 'n_itens': carrinho.total_itens()}
	simplejson.dump(context, response)
	return response

@csrf_exempt
def remove_do_carrinho(request):
	if not request.is_ajax():
		return HttpResponseForbidden('<h1>Permissão negada!</h1>')
	
	item_id = int(request.POST.get('id'))
	response = HttpResponse()
	carrinho = get_carrinho(request)
	item_id = carrinho.get_item_id(item_id)
	carrinho.remove_item(item_id)
	context = {'total': carrinho.valor_total(), 'msg': 'O item foi removido', 'n_itens': carrinho.total_itens()}
	simplejson.dump(context, response)
	return response

@csrf_exempt
def edita_carrinho(request):
	if not request.is_ajax():
		return HttpResponseForbidden('<h1>Permissão negada!</h1>')
	
	item_id = int(request.POST.get('id'))
	quantidade = int(request.POST.get('quantidade'))
	response = HttpResponse()
	carrinho = get_carrinho(request)
	item_id = carrinho.get_item_id(item_id)
	item = carrinho.get_item(item_id)
	if carrinho.pode_editar(item, quantidade):
		carrinho.adiciona_item(item.produto, quantidade, edita=True)
		context = {'total': carrinho.valor_total(), 'msg': 'O item foi alterado', 'n_itens': carrinho.total_itens()}
	else:
		context = {'msg':'N&atilde;o h&aacute; estoque suficiente para a quantidade pedida.', 'n_itens': carrinho.total_itens()}
	simplejson.dump(context, response)
	return response

def finaliza_pedido(request):
	carrinho = get_carrinho(request)
	'''if not request.user.cliente.valida():
		return HttpResponseRedirect(reverse('meus_dados'))'''
	pedido = carrinho.cria_pedido(request.user)
	url_sucesso = request.build_absolute_uri(reverse('finaliza_pedido'))
	url_cancelamento = request.build_absolute_uri(reverse('carrinho'))
	#	
	carrinho_pagseguro = Pagseguro(email_cobranca=settings.EMAIL_PAGSEGURO, ref_transacao=pedido.pk, tipo_frete='EN', tipo='CP')
	carrinho_pagseguro.cliente(nome=pedido.cliente.get_full_name(), cep=pedido.cliente.cliente.cep)
	for item in pedido.produtos.all():
		carrinho_pagseguro.item(id=item.pk, desc=item.produto.nome, quant=item.quantidade, valor=item.produto.preco, peso=item.produto.peso/1000)
	link_pagseguro = carrinho_pagseguro.mostra()
	#
	carrinho_paypal = PayPal()
	token_paypal = carrinho_paypal.SetExpressCheckout('%.2f' % pedido.valor_total, url_sucesso, url_cancelamento)
	token_paypal = carrinho_paypal.GetExpressCheckoutDetails(token_paypal)
	link_paypal = carrinho_paypal.PAYPAL_URL+token_paypal
	carrinho_paypal.GetExpressCheckoutDetails(token_paypal)
	#
	return render_to_response('pedidos/finaliza_pedido.html', locals(), context_instance=RequestContext(request))