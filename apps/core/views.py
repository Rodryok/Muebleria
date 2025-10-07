from datetime import date
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Categoria, DetalleRemito, Producto
from apps.core import models

from django.db.models import Q
from datetime import date
# Create your views here.



# vista  basadas en funciones 
def hola_mundo(request): 
    return HttpResponse("hola mundo desde una vista basada en funciones")

# vista basadas en class
class HolaMundoView(View):
    def get(self,request): 
        return HttpResponse("Hola Mundo desde una vista basada en clase")

# def index(request): 
#     return render(request,'template/index.html',{'mensaje':'BIENVENIDO A CLUB ADMIN'})
   
# def index(request): 
#     SALUDO = "bienvenidos"
#     return HttpResponse('<i>'+SALUDO+'</i>')

# def index(request): 
#     SALUDO = "bienvenidos"
#     arreglo = [' luis ',' ana ',' juan ',' karla ']
#     return HttpResponse(arreglo)

# def index(request): 
#     contexto = {
#         'mensaje':'BIENVENIDO A CLUB ADMIN'
#     }
#     return render(request,'index.html',contexto)


def index(request): 
    lista_persona = [
         [' jorge ','23.256.256',30],
         [' luis ','19.568.468',44],
         [' ana ','30.256.256',38],
         [' maria ','45.125.125',26],
    ]
   
    contexto = {
        'nombre': 'jorge',
        'edad': 30,
        'lista_persona': lista_persona,
        'saludo':'BIENVENIDO A CLUB ADMIN'
    }
    return render(request,'index.html',contexto)
def home(request):
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria')

    items = Producto.objects.select_related('categoria', 'proveedor').filter(activo=True)

    if query:
        items = items.filter(nombre__icontains=query)

    if categoria_id and categoria_id.isdigit():
        items = items.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()

    contexto = {
        'items': items,
        'query': query,
        'categoria_id': categoria_id,
        'categorias': categorias
    }
    return render(request, 'home.html', contexto)

# def index(request): 
#     auto = {'marca':'fiat', 'patente': 'afsg5757', 'modelo':'cronos' }
#     print(auto)
#     return render(request,"index.html", {"auto": auto})


# def loginView(request):
#     saludo = "BIENVENIDO A LA PÁGINA DE INICIO DE SESIÓN,POR FAVOR INGRESE SUS DATOS"
#     return render(request, "login.html", {'saludo': saludo})

def loginView(request):
    # print(request.GET)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"Usuario: {username}, Contraseña: {password}")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            # print("Inicio de sesión exitoso")
            # return render(request, "home.html")
        else:
            mensaje = "Credenciales inválidas, por favor intente de nuevo."
            contexto = {
                'mensaje': mensaje
            }
            print("Credenciales inválidas")
            return render(request, "login.html", contexto)
        
    contexto = {
    }
    return render(request, "login.html", contexto)


def base(request):
    return render(request, "base.html")
   
# def dashboard(request):
#     productos = Producto.objects.select_related('categoria', 'proveedor').all()

#     total_productos = productos.count()
#     stock_bajo = 0
#     total_categorias = Categoria.objects.count()
#     ventas_hoy = 0
#     hoy = date.today()

#     contexto = {
#         'productos': productos,
#         'total_productos': total_productos,
#         'stock_bajo': stock_bajo,
#         'total_categorias': total_categorias,
#         'ventas_hoy': ventas_hoy
#     }
#     return render(request, 'dashboard.html', contexto)

def dashboard(request):
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria')

    productos = Producto.objects.select_related('categoria', 'proveedor').filter(activo=True)

    if query:
        productos = productos.filter(nombre__icontains=query)

    if categoria_id and categoria_id.isdigit():
        productos = productos.filter(categoria_id=categoria_id)

    total_productos = productos.count()
    stock_bajo = 0
    total_categorias = Categoria.objects.count()
    ventas_hoy = 0  

    categorias = Categoria.objects.all()

    contexto = {
        'productos': productos,
        'total_productos': total_productos,
        'stock_bajo': stock_bajo,
        'total_categorias': total_categorias,
        'ventas_hoy': ventas_hoy,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id
    }
    return render(request, 'dashboard.html', contexto)

def logoutView(request):
    logout(request)
    return redirect('home')