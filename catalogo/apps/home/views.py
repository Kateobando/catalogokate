from catalogo.apps.home.forms import contact_forms, Login_form, RegisterForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from catalogo.apps.ventas.models import Producto , Marca , Categoria
from django.core.paginator import Paginator, EmptyPage, InvalidPage 
from django.contrib.auth.models import User 



def about_view (request):
	return render_to_response('home/about.html', context_instance = RequestContext(request) )

def index_view (request):
	return render_to_response('home/index.html', context_instance = RequestContext(request) )

def contact_view (request):
	formulario = contact_forms()
	ctx = {'form':formulario}
	return render_to_response('home/contacto.html',ctx,context_instance = RequestContext(request) )

def contacto_view (request):
	info_enviado = False #Definir  si se envio la informacion o no se envio
	email = ""
	title = ""
	text  = ""
	if request.method == "POST": # evalua si el metodo fue POST
		formulario = contact_forms(request.POST) #intancia del formulario con los datos ingresados
		if formulario.is_valid(): #evalua si el fomulario es valido
			info_enviado = True #la informacion se envio correctamente
			email = formulario.cleaned_data['correo'] #copia el correo ingresado en email
			title = formulario.cleaned_data['titulo'] # copia el titulo ingresado en title 
	else: #si no fue POST entonces fue  el metodo GET mostrara un formulario vacio
		formulario = contact_forms() # creacion del formulario vacio
	ctx = {'form':formulario, 'email':email, "title":title, "text":text, "info_enviado":info_enviado} 
	return render_to_response('home/contacto.html',ctx,context_instance = RequestContext(request))

def single_product_view(request, id_prod):
	prod = Producto.objects.get(id = id_prod)
	ctx = {'producto':prod}
	return render_to_response('home/single_producto.html',ctx,context_instance = RequestContext(request))


def single_marca_view(request, id_prod):
	prod = Marca.objects.get(id = id_prod)
	ctx = {'marca':prod}
	return render_to_response('home/single_marca.html',ctx,context_instance = RequestContext(request))

def single_categoria_view(request, id_prod):
	prod = Categoria.objects.get(id = id_prod)
	ctx = {'categoria':prod}
	return render_to_response('home/single_categoria.html',ctx,context_instance = RequestContext(request))	

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else: 
		if request.method == "POST":
			formulario = Login_form(request.POST)
			if formulario.is_valid():
				usu = formulario.cleaned_data['usuario']
				pas = formulario.cleaned_data['clave']
				usuario = authenticate(username = usu, password = pas)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o clave incorrecta"
		formulario = Login_form()
		ctx = {'form':formulario, 'mensaje':mensaje}
		return render_to_response('home/login.html', ctx, context_instance = RequestContext(request))				

def logout_view(request):
 	logout(request)
 	return HttpResponseRedirect('/')

def productos_view(request, pagina):
	lista_prod = Producto.objects.filter(status = True)
	#lista_prod = Producto.objects.filter(precio = 3100)
	#lista_prod = Producto.objects.filter(marca__nombre = 'Colgate')

	paginator = Paginator(lista_prod, 3)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage,InvalidPage):
		productos = paginator.page(paginator.num_pages)

	ctx = {"productos":productos}
	return render_to_response ('home/productos.html', ctx, context_instance = RequestContext(request))

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save()
			return render_to_response('home/thanks_register.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))