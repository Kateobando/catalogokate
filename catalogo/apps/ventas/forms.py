from django import forms 
from catalogo.apps.ventas.models import Producto,Marca,Categoria

class add_product_form(forms.ModelForm):
	class Meta:
		model   = Producto
		exclude = {'status',}
	
class add_marca_form(forms.ModelForm):
	class Meta:
		model   = Marca 

class add_categoria_form(forms.ModelForm):
	class Meta:
		model   = Categoria  	