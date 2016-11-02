from django.conf.urls import *

urlpatterns = patterns('produtos.views',
	url(r'^$', 'categorias', name='categorias'),
	url(r'^busca/$', 'busca', name='busca'),
	url(r'^(?P<slug_categoria>[-\w]+)/$', 'categorias_produto', name='categorias_produto'),
	url(r'^(?P<slug_categoria>[-\w]+)/produtos/$', 'produtos', name='produtos'),
	url(r'^(?P<slug_categoria>[-\w]+)/produtos/(?P<slug>[-\w]+)/$', 'detalhe_produto', name='detalhe_produto')
)
