import os
from django.template import Library, Node, resolve_variable, TemplateSyntaxError
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from modulos.models import Pagina, Modulo, ComponentePagina
from utils.quick_tag import quick_tag

register = Library()

'''
@register.tag('create_search_box')
@quick_tag
def create_search_box(context, tag_name):
	try:
		conteudo = render_to_string('includes/busca.html', {'search_form': FormBusca(), 'csrf_token': context.get('csrf_token')})
		conteudo = conteudo.strip(u'\ufeff').strip()
		return mark_safe(conteudo)
	except:
		return ''
'''
		
@register.tag('get_componentes_modulo')
@quick_tag
def get_componentes_modulo(context, modulo_id, parts):
	try:
		conteudo = ''
		usuario = context['user']
		try:
			url = context['request'].path.split('/')
			url = '/'.join(url[:parts])
			if url == '/':
				pagina = Pagina.objects.get(url=url)
			else:
				pagina = Pagina.objects.get(url__startswith=url)
			modulo = Modulo.objects.get(id_css=modulo_id)
		except:
			conteudo = ''
		componentes = ComponentePagina.objects.filter(pagina=pagina, modulo=modulo)
		if not componentes:
			conteudo = ''
		if usuario.is_authenticated():
			if usuario.is_staff:
				componentes = componentes.filter(administradores=True)
			else:
				componentes = componentes.filter(usuarios_registrados=True)
		else:
			componentes = componentes.filter(visitantes=True)
		if componentes.count > 0:
			componentes = componentes.order_by('ordem')
			for componente in componentes:
				html = componente.componente.render(context).strip(u'\ufeff').strip()
				conteudo += html
		return mark_safe(conteudo)
	except:
		return ''