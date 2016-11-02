# -*-coding: utf-8 -*-
from datetime import datetime
from pedidos.models import Pedido, ProdutoPedido, ItemCarrinho
from produtos.models import Produto

class Carrinho(object):
	def __init__(self, carrinho):
		self.carrinho = carrinho

	def adiciona_item(self, produto, quantidade=1, edita=False):
		itemExistente = None
		for i in self:
			if i.produto == produto:
				itemExistente = i
				break

		if itemExistente:
			self.remove_item(itemExistente.id)
		
		produto = Produto.objects.get(id=produto.id)
		item = ItemCarrinho()
		item.carrinho = self.carrinho
		item.produto = produto
		if itemExistente and not edita:
			item.quantidade = quantidade + itemExistente.quantidade
			produto.retira_estoque(quantidade + itemExistente.quantidade)
		else:
			item.quantidade = quantidade
			produto.retira_estoque(quantidade)
		item.save()

	def pode_editar(self, item, quantidade):
		if (item.produto.quantidade_estoque + item.quantidade - quantidade) >= 0:
			return True
		return False

	def vazio(self):
		return self.carrinho.itens.count == 0

	def get_item_id(self, item_idx):
		return self.carrinho.itens.all()[item_idx-1].id

	def get_item(self, item_id):
		return self.carrinho.itens.get(id=item_id)

	def limpar(self):
		for item in self.carrinho.itens.all():
			item.produto.adiciona_estoque(item.quantidade)
			item.delete()
		
	def remove_item(self, item_id):
		item = self.carrinho.itens.get(id=item_id)
		item.produto.adiciona_estoque(item.quantidade)
		item.delete()
		
	def __iter__(self):
		for item in self.carrinho.itens.all():
			yield item

	def valor_total(self):
		total = 0.0
		for item in self.carrinho.itens.all():
			total += float(item.valor_total)
		return total
		
	def total_itens(self):
		return self.carrinho.itens.count()

	def cria_pedido(self, cliente=None):
		pedido = Pedido.objects.create(cliente=cliente, status='A')
		pedido.save()
		for item in self.carrinho.itens.all():
			item_pedido = ProdutoPedido(pedido=pedido, produto=item.produto, quantidade=item.quantidade, valor_unitario=item.produto.get_preco())
			item_pedido.save()
		self.limpar()
		return pedido	