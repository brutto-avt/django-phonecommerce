# -*-coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produto
from datetime import datetime
from statics import STATUS_CHOICES

class Pedido(models.Model):
	cliente = models.ForeignKey(User, blank=True, null=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)
	data_criacao = models.DateTimeField(default=datetime.now())
	commentarios = models.TextField(blank=True)

	@property
	def valor_total(self):
		total = 0.0
		for produto in self.produtos.all():
			total += float(produto.valor_total)
		return total
		
	def __unicode__(self):
		return u'%s <%s @ %s>' % (self.cliente, self.valor_total, self.data_criacao)

class ProdutoPedido(models.Model):
	pedido = models.ForeignKey(Pedido, related_name='produtos')
	produto = models.ForeignKey(Produto, related_name='itens_pedido')
	valor_unitario = models.DecimalField(max_digits=7, decimal_places=2)
	quantidade = models.PositiveIntegerField()
	commentarios = models.TextField(blank=True)

	@property
	def valor_total(self):
		return self.quantidade * self.produto.preco

class Carrinho(models.Model):
	cliente = models.ForeignKey(User, blank=True, null=True, related_name='carrinho')
	criacao = models.DateTimeField(default=datetime.now())
	finalizado = models.BooleanField(default=False)

	class Meta:
		get_latest_by = 'criacao'

class ItemCarrinho(models.Model):
	carrinho = models.ForeignKey(Carrinho, related_name='itens')
	produto = models.ForeignKey(Produto)
	quantidade = models.PositiveIntegerField()

	def _get_valor_total(self):
		return self.quantidade * self.produto.get_preco()
	valor_total = property(_get_valor_total)

	def __unicode__(self):
		return self.produto.nome