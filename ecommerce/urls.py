from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'ecommerce.views.index', {}, 'index'),
	(r'^contato/$', 'ecommerce.views.contato'),
	(r'^registro/$', 'ecommerce.views.registro'),
	(r'^login/$', 'ecommerce.views.login'),
	(r'^logout/$', 'ecommerce.views.logout'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^admin_tools/', include('admin_tools.urls')),
	(r'loja/', include('produtos.urls')),
	(r'clientes/', include('clientes.urls')),
	(r'carrinho/', include('pedidos.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
