# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from clientes.models import Cliente
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from clientes.forms import FormCliente
from pedidos.views import get_carrinho

@login_required
def meus_dados(request):
	cliente = Cliente.objects.filter(user__id=request.user.id)
	carrinho = get_carrinho(request)
	if cliente.count() == 0:
		perfil = Cliente()
		cliente.user = request.user
		cliente.save()
	else:
		cliente = cliente[0]
	form = FormCliente(instance=cliente)
	if request.method == 'POST':
		form = FormCliente(request.POST, instance=cliente)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('meus_dados'))
				
	return render_to_response('clientes/editar_dados.html', locals(), context_instance=RequestContext(request))