from django.contrib import admin
from produtos.models import *
from produtos.forms import FormAdminProduto
from produtos.models import DetalheProduto

class DetalhesInline(admin.TabularInline):
	model = DetalheProduto
	extra = 3

class CategoriaProdutoAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'descricao', 'pai')

class ProdutoAdmin(admin.ModelAdmin):
	form = FormAdminProduto
	list_display = ('nome', 'descricao', 'categoria', 'quantidade_estoque',)
	exclude = ['thumb',]
	fieldsets = (
		(None, {
			'fields': ('categoria', 'nome', 'slug', 'descricao', 'original', 'imagem_slide', 'fabricante', 'quantidade_estoque',)
		}),
		('Valores de Frete', {
			'classes': ('wide',),
			'fields': ('preco', 'preco_desconto', 'limite_desconto', 'peso', 'largura', 'altura', 'comprimento')
		}),
	)
	inlines = [DetalhesInline]

class DetalheProdutoAdminAdmin(admin.ModelAdmin):
	list_display = ('produto', 'atributo', 'valor')

class AtributoProdutoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'descricao')

admin.site.register(CategoriaProduto, CategoriaProdutoAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(DetalheProduto, DetalheProdutoAdminAdmin)
admin.site.register(AtributoProduto, AtributoProdutoAdmin)