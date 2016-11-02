from django.template.defaultfilters import slugify
from imagem import corta_imagem

try:
	import Image
except ImportError:
	from PIL import Image

def thumb_post_save(signal, instance, sender, **kwargs):
	if not instance.thumb:
		if instance.original:
			extensao = instance.original.name.split('.')[-1]
			instance.thumb = '%s/%s.%s' % (instance.thumb.field.upload_to, instance.id, extensao)
			miniatura = Image.open(instance.original.path)
			miniatura = corta_imagem(miniatura, (50,83))
			miniatura.save(instance.thumb.path)
			instance.save()
			
def slug_pre_save(signal, instance, sender, **kwargs):
	slug = None
	
	if not instance.slug:
		try:
			slug = slugify(instance.titulo)
		except:
			slug = slugify(instance.nome)
		novo_slug = slug
		contador = 0
		
		while sender.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
			contador += 1
			novo_slug = '%s-%d' % (slug, contador)
		
		instance.slug = novo_slug