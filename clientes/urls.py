from django.conf.urls import *

urlpatterns = patterns('clientes.views',
	url(r'^$', 'meus_dados', name='meus_dados'),
)