# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms
from django.core.mail import send_mail

class FormRegistro(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'password')
		widgets = {
			'password': forms.widgets.PasswordInput(),
		}

class FormLogin(forms.Form):
	usuario = forms.CharField(max_length=50)
	senha = forms.CharField(max_length=50, widget=forms.PasswordInput)

class FormContato(forms.Form):
	nome = forms.CharField(max_length=50)
	email = forms.EmailField(required=False)
	mensagem = forms.Field(widget=forms.Textarea)
	
	def enviar(self):
		titulo = 'Mensagem enviada pelo site'
		destino = 'lcn.andre@gmail.com'
		remetente = 'andre-avt@bol.com.br'
		texto = """
		Nome: %(nome)s
		E-mail: %(email)s
		Mensagem:
		%(mensagem)s
		""" % self.cleaned_data
		
		send_mail(subject=titulo, message=texto, from_email=remetente, recipient_list=[destino],)