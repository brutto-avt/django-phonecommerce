from django.conf.urls import *
from produtos.models import Produto

urlpatterns = patterns('pedidos.views',
	url(r'^$', 'carrinho', name='carrinho'),
	url(r'^config/$', 'carrinho_config', name='carrinho_config'),
	url(r'^json/$', 'carrinho_json', name='carrinho_json'),	
	url(r'^adiciona/(?P<slug_produto>[-\w]+)/$', 'adicionar_ao_carrinho', name='adicionar_ao_carrinho'),
	url(r'^remove/$', 'remove_do_carrinho', name='remove_do_carrinho'),
	url(r'^edita/$', 'edita_carrinho', name='edita_carrinho'),
	url(r'^finaliza/$', 'finaliza_pedido', name='finaliza_pedido')
)
