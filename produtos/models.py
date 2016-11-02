# -*-coding: utf-8 -*-
from django.db import models
from django.utils.timezone import utc
from datetime import datetime
from django.db.models import signals

from utils.signals_comuns import thumb_post_save, slug_pre_save

class CategoriaProduto(models.Model):
	pai = models.ForeignKey('self', blank=True, null=True, related_name='filhos')
	nome = models.CharField(max_length=300)
	slug = models.SlugField(max_length=150, unique=True, blank=True, help_text='Este campo é gerado automaticamente se deixado em branco')
	descricao = models.TextField(blank=True)

	def contem_filhos(self):
		if self.filhos.count() > 0:
			return True
		return False
	
	def vazia(self):
		if not self.contem_filhos():
			if self.produtos.count() > 0:
				return False
		else:
			for sub in self.filhos.all():
				if not sub.vazia():
					return False
		return True
	
	def __unicode__(self):
		if self.pai:
			return u'%s - %s' % (self.pai.nome, self.nome)
		return u'%s' % (self.nome)
		
	@models.permalink
	def get_absolute_url(self):
		if self.filhos.count() > 0:
			return ('categorias', (), {'slug_categoria': self.slug})
		return ('produtos', (), {'slug_categoria': self.slug})

	class Meta:
		verbose_name = 'Categoria de produto'
		verbose_name_plural = 'Categorias de produto'
		
class Produto(models.Model):
	categoria = models.ForeignKey('CategoriaProduto', related_name='produtos')
	nome = models.CharField(max_length=300)
	slug = models.SlugField(max_length=150, unique=True, blank=True, help_text='Este campo é gerado automaticamente se deixado em branco')
	descricao = models.TextField()
	resumo = models.CharField(max_length=300)
	original = models.ImageField(upload_to='produtos/original', blank=True, null=True, verbose_name='Foto')
	imagem_slide = models.ImageField(upload_to='produtos/slide', blank=True, null=True, verbose_name='Imagem slide')
	thumb = models.ImageField(upload_to='produtos/thumb', null=True, blank=True)
	fabricante = models.CharField(max_length=300, blank=True)
	preco = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Preço', help_text='Separe os centavos com ponto')
	preco_desconto = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Preço com desconto', help_text='Separe os centavos com ponto', blank=True, null=True)
	limite_desconto = models.DateTimeField(blank=True, null=True)
	peso = models.DecimalField(max_digits=3, decimal_places=2, help_text='Em Kg')
	largura = models.DecimalField(max_digits=4, decimal_places=2, help_text='Em cm')
	altura = models.DecimalField(max_digits=4, decimal_places=2, help_text='Em cm')
	comprimento = models.DecimalField(max_digits=4, decimal_places=2, help_text='Em cm')
	quantidade_estoque = models.IntegerField(verbose_name='Quantidade em estoque')

	def pode_vender(self, quantidade):
		if self.quantidade_estoque - quantidade >= 0:
			return True
		return False

	def adiciona_estoque(self, quantidade):
		self.quantidade_estoque += quantidade
		self.save()
	
	def retira_estoque(self, quantidade):
		self.quantidade_estoque -= quantidade
		self.save()
	
	def __unicode__(self):
		return u'%s' % self.nome

	@property
	def descricao_slider(self):
		if len(self.descricao) > 120:
			return self.descricao[:120] + '...'
		else:
			return self.descricao

	def get_preco(self):
		if self.preco_desconto:
			if self.limite_desconto:
				if self.limite_desconto >= datetime.utcnow().replace(tzinfo=utc):
					return self.preco_desconto
				else:
					return self.preco
			return self.preco_desconto
		return self.preco

	@models.permalink
	def get_absolute_url(self):
		return ('detalhe_produto', (), {'slug_categoria': self.categoria.slug, 'slug': self.slug})

class DetalheProduto(models.Model):
	produto = models.ForeignKey('Produto', related_name='detalhes')
	atributo = models.ForeignKey('AtributoProduto')
	valor = models.CharField(max_length=500)
	descricao = models.TextField(blank=True)

	def __unicode__(self):
		return u'%s: %s' % (self.produto, self.atributo)

	class Meta:
		verbose_name = 'Detalhe de produto'
		verbose_name_plural = 'Detalhes de produto'

class AtributoProduto(models.Model):
	nome = models.CharField(max_length=300)
	descricao = models.TextField(blank=True)

	def __unicode__(self):
		return u'%s' % self.nome

	class Meta:
		verbose_name = 'Atributo de produto'
		verbose_name_plural = 'Atributos de produto'
		
#SIGNALS
signals.post_save.connect(thumb_post_save, sender=Produto)
signals.pre_save.connect(slug_pre_save, sender=Produto)
signals.pre_save.connect(slug_pre_save, sender=CategoriaProduto)