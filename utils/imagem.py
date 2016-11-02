import os
from django.conf import settings

try:
	import Image
except ImportError:
	from PIL import Image

def corta_imagem(imagem, tamanho):
	thumb = imagem.resize(tamanho, Image.ANTIALIAS)
	return thumb