# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from clientes.fields import AutoOneToOneField
from django_localflavor_br.br_states import STATE_CHOICES

class Cliente(models.Model):
	user = user = AutoOneToOneField(User, primary_key=True, verbose_name='Usuário')
	telefone = models.CharField(max_length=15, blank=True)
	cep = models.CharField(max_length=10, verbose_name='CEP')
	uf = models.CharField(max_length=2, choices=STATE_CHOICES, verbose_name='UF')
	cidade = models.CharField(max_length=300)
	bairro = models.CharField(max_length=300)
	rua = models.CharField(max_length=300)
	numero = models.CharField(max_length=30, verbose_name=u'Número')
	complemento = models.CharField(max_length=300, blank=True)  

	def valida(self):
		try:
			if len(self.uf.trim()) == 0:
				return False
			if len(self.cidade.trim()) == 0:
				return False
			if len(self.bairro.trim()) == 0:
				return False
			if len(self.rua.trim()) == 0:
				return False
			if len(self.numero.trim()) == 0:
				return False
			if len(self.cep.trim()) == 0:
				return False
		except:
			return False
		return True


	def __unicode__(self):
		return u'%s' % self.user.get_full_name()