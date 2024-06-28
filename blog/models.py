from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class ModelBlogBase(models.Model):
	id = models.AutoField(primary_key = True)
	status = models.BooleanField('Estado', default=True)
	creation_date = models.DateField('Fecha de Creación', auto_now=False, auto_now_add=True)
	modified_date = models.DateField('Fecha de Modificación', auto_now=True, auto_now_add=False)
	deleted_date = models.DateField('Fecha de Eliminación', auto_now=True, auto_now_add=False)

	class Meta:
		abstract = True


class Category(ModelBlogBase):
	name = models.CharField('Nombre de la Categoría', max_length=100, unique=True)
	image = models.ImageField('Imagen Referencial',upload_to='categoria/')

	class Meta:
		verbose_name = 'Categoría'
		verbose_name_plural = 'Categorías'

	def __str__(self):
		return self.name


class Author(ModelBlogBase):
	name = models.CharField('Nombres', max_length=100)
	last_name = models.CharField('Apellidos', max_length=120)
	email = models.EmailField('Correo Electrónico', max_length=200)
	description = models.TextField('Descripción')
	image = models.ImageField('Imagen Referencial', null=True, blank=True,upload_to = 'autores/')


	class Meta:
		verbose_name = 'Autor'
		verbose_name_plural = 'Autores'

	def __str__(self):
		return '{0}, {1}'.format(self.last_name, self.name)


class Post(ModelBlogBase):
	title = models.CharField(max_length=150, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField('Descripción')
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	content = CKEditor5Field('Text', config_name='extends')
	image = models.ImageField('Imagen Referencial', upload_to='imagenes/', max_length=255)
	is_publicated = models.BooleanField('Publicado / No Publicado',default=False)
	publicated_date = models.DateField('Fecha de Publicación')

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'
		ordering = ('-publicated_date',)

	def __str__(self):
		return self.title
