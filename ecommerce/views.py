# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from pedidos.views import get_carrinho
from pedidos.models import Carrinho
from produtos.models import Produto
from ecommerce.forms import FormContato, FormRegistro, FormLogin

def index(request):
	carrinho = get_carrinho(request)
	produtos = Produto.objects.all().order_by('nome')
	return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def contato(request):
	carrinho = get_carrinho(request)
	if request.method == 'POST':
		form = FormContato(request.POST)
		
		if form.is_valid():
			form.enviar()
			mensagem = 'Mensagem enviada com sucesso.<br />Obrigado pelo contato!'
	else:
		form = FormContato()
	return render_to_response('contato.html', locals(), context_instance=RequestContext(request))

def registro(request):
	carrinho = get_carrinho(request)
	if request.method == 'POST':
		form = FormRegistro(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			mensagem = 'Cadastro efetuado com sucesso.'
			return render_to_response('registro.html', locals(), context_instance=RequestContext(request))
	else:
		form = FormRegistro()
	return render_to_response('registro.html', locals(), context_instance=RequestContext(request))

def login(request):
	if request.method == 'POST':
		form = FormLogin(request.POST)
		if form.is_valid:
			user = authenticate(username=request.POST['usuario'], password=request.POST['senha'])
			if user is not None:
				if user.is_active:
					try:
						ultimo_carrinho = Carrinho.objects.filter(cliente=user, finalizado=False).latest()
						request.session['carrinho_id'] = ultimo_carrinho.id
					except:
						pass
					django_login(request, user)
					return HttpResponseRedirect('/')
			else:
				mensagem = 'Dados incorretos.'
	else:
		form = FormLogin()
	return render_to_response('login.html', locals(), context_instance=RequestContext(request))

def logout(request):
	django_logout(request)
	return HttpResponseRedirect('/')