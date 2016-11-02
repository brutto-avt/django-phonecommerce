from haystack.indexes import *
from haystack import site

from produtos.models import Produto

class ProdutoIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	nome = CharField(model_attr='nome')
	descricao = CharField(model_attr='descricao')
	fabricante = CharField(model_attr='fabricante')
	
	def index_queryset(self):
		return Produto.objects.all()
		
site.register(Produto, ProdutoIndex)