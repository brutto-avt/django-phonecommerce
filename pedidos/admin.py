# -*-coding: utf-8 -*-
from django.contrib import admin
from pedidos.models import Pedido, ProdutoPedido

class ProdutoPedidoAdmin(admin.ModelAdmin):
	model = ProdutoPedido
	list_display = ('produto', 'pedido', 'quantidade',)

class ProdutoPedidoInline(admin.TabularInline):
	model = ProdutoPedido

class PedidoAdmin(admin.ModelAdmin):
	model = Pedido
	inlines = [ProdutoPedidoInline]

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ProdutoPedido, ProdutoPedidoAdmin)