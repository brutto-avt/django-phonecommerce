# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import signals
from utils.signals_comuns import slug_pre_save

class Menu(models.Model):
	titulo = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, unique=True, blank=True, help_text='Este campo é gerado automaticamente se deixado em branco')
	classe_css = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.titulo
	
class ItemMenu(models.Model):
	menu = models.ForeignKey('Menu')
	titulo = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, unique=True, blank=True, help_text='Este campo é gerado automaticamente se deixado em branco')
	link = models.CharField(max_length=255)
	pai = models.ForeignKey('ItemMenu', blank=True, null=True)
	ordem = models.PositiveIntegerField(db_index=True, default=0)
	visitantes = models.BooleanField(default=True)
	usuarios_registrados = models.BooleanField(default=True)
	administradores = models.BooleanField(default=True)
	nova_janela = models.BooleanField(u'Abrir em nova janela/aba?', default=False)
	classe_css = models.CharField(max_length=30, blank=True, null=True)
	
	def filhos(self):
		return ItemMenu.objects.filter(pai=self)
	
	def __unicode__(self):
		return self.titulo
	
	class Meta:
		ordering = ('menu', 'ordem')
		verbose_name = 'Item de menu'
		verbose_name_plural = 'Itens de menu'
		
#SIGNALS
signals.pre_save.connect(slug_pre_save, sender=Menu)
signals.pre_save.connect(slug_pre_save, sender=ItemMenu)