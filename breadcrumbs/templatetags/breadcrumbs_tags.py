from django.template import Library
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from utils.quick_tag import quick_tag

register = Library()

@register.tag('get_breadcrumbs')
@quick_tag
def get_breadcrumbs(context):
	try:
		conteudo = ''
		url_dict = {}
		try:
			url = context['request'].path.split('/')
			if len(url) == 1:
				return ''
			else:
				url = url[1:-1]
				for part in url:
					idx = context['request'].path.find(part)+len(part)
					link = context['request'].path[:idx+1]
					url_dict[link] = part.replace('-',' ').title()
				html = render_to_string('breadcrumbs/breadcrumbs.html', {'url_dict': url_dict})
				return mark_safe(html)
		except:
			return ''
	except:
		return ''

@register.filter('get_key')
def get_key(dict, key):
	return dict[key]