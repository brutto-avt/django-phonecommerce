# -*- coding: utf-8 -*-
from django import forms
from django_localflavor_br.forms import BRZipCodeField, BRPhoneNumberField, BRStateSelect
from datetime import datetime
from clientes.models import Cliente
		
class FormCliente(forms.ModelForm):
	class Meta:
		model = Cliente
		fields = ('telefone', 'cep', 'uf', 'cidade', 'bairro', 'rua', 'numero', 'complemento')
		
	def __init__(self, *args, **kwargs):
		self.base_fields['uf'].widget = BRStateSelect()
		self.user = kwargs['instance'].user
		super(FormCliente, self).__init__(*args, **kwargs)
		
	def save(self, commit=True):
		super(FormCliente, self).save(commit=True)