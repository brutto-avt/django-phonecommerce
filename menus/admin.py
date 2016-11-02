# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Menu, ItemMenu
from django.contrib.admin.options import ModelAdmin

class MenuAdmin(ModelAdmin):
	list_display = ('titulo', 'slug')
	search_fields = ('titulo',)

class ItemMenuAdmin(ModelAdmin):
	list_display = ('menu', 'ordem', 'titulo', 'slug', 'pai', 'link',)
	search_fields = ('titulo', 'pai', 'link',)
	fieldsets = (
		(None, {'fields': ('menu', 'titulo', 'slug', 'link', 'pai', 'ordem', 'classe_css', 'nova_janela',)}),
		('Permissões', {'fields': ('visitantes', 'usuarios_registrados', 'administradores')}),
	)

admin.site.register(Menu, MenuAdmin)
admin.site.register(ItemMenu, ItemMenuAdmin)