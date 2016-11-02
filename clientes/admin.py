# -*- coding: utf-8 -*-
from django.contrib import admin
from clientes.models import Cliente

class ClienteAdmin(admin.ModelAdmin):
	list_display = ('user', 'telefone', 'uf', 'cidade',)
	fieldsets = (
		(None, {
			'fields': ('user', 'telefone')
		}),
		(u'Endereço', {
			'classes': ('wide',),
			'fields': ('cep', 'uf', 'cidade', 'bairro', 'rua', 'numero', 'complemento')
		}),
	)

admin.site.register(Cliente, ClienteAdmin)