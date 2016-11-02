# -*- coding: utf-8 -*-
from django import forms
from produtos.models import Produto

class FormAdminProduto(forms.ModelForm):
	def save(self, commit=True):
		prod = super(FormAdminProduto, self).save(commit=False)
		#Validação da categoria
		if prod.categoria.contem_filhos():
			raise forms.ValidationError(u'Impossivel incluir produtos nesta categoria, pois ela contem sub-categorias')
		#Gravação
		if commit:
			prod.save()
		return prod
	
	class Meta:
		model = Produto