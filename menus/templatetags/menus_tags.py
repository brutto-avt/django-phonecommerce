# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from menus.models import Menu
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from utils.quick_tag import quick_tag

register = template.Library()

@register.tag('menu')
@quick_tag
def menu(context, slug=None):
	try:
		menu = Menu.objects.get(slug=slug)
		itens = menu.itemmenu_set.filter(pai=None)
		html = template.loader.render_to_string('menus/menu.html', {
			'menu': menu,
			'itens': itens,
			'user': context['user'],
			'request': context['request']
		})
		return mark_safe(html.strip(u'\ufeff').strip())
	except:
		return ''

@register.tag('item_menu')
@quick_tag
def item_menu(context, item, counter):
	continua = True
	try:
		if not item.visitantes:
			if item.usuarios_registrados and not context['user'].is_authenticated():
				continua = False
			elif item.administradores and not context['user'].is_staff:
				continua = False
			
		if continua:
			try:
				path = context['request'].path
			except:
				path = None
			
			classe = None
			if path and path == item.link:
				classe = "on"
			if counter == 1:
				if classe:
					classe += " first"
				else:
					classe = "first"

			html = render_to_string('menus/item_menu.html', {
				'item': item,
				'classe': classe,
				'user': context['user'],
				'request': context['request']
			})
			return mark_safe(html.strip(u'\ufeff').strip())
		return ''
	except:
		return ''
