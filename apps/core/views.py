from datetime import date
from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from apps.core.form import ClienteForm, DetalleRemitoForm, ProductoForm, ProveedorForm, RemitoForm, CategoriaForm
from .models import Categoria, DetalleRemito, Producto, Proveedor, Remito, Cliente
from apps.core import models
from django.db import transaction



def home(request):
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria')
    orden = request.GET.get('orden')

    items = Producto.objects.select_related('categoria', 'proveedor').filter(activo=True)

    if query:
        items = items.filter(nombre__icontains=query)

    if categoria_id and categoria_id.isdigit():
        items = items.filter(categoria_id=categoria_id)

    if orden == 'nombre_asc':
        items = items.order_by('nombre')
    elif orden == 'nombre_desc':
        items = items.order_by('-nombre')
    elif orden == 'precio_menor':
        items = items.order_by('precio')
    elif orden == 'precio_mayor':
        items = items.order_by('-precio')
    elif orden == 'stock':
        items = items.order_by('-stock')

    categorias = Categoria.objects.all()

    contexto = {
        'items': items,
        'query': query,
        'categoria_id': categoria_id,
        'categorias': categorias
    }

    return render(request, 'home.html', contexto)



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
    proveedores = Proveedor.objects.filter(activo=True)
    remitos = Remito.objects.all().order_by('-fecha')  # <-- agregamos los remitos

    contexto = {
        'productos': productos,
        'total_productos': total_productos,
        'stock_bajo': stock_bajo,
        'total_categorias': total_categorias,
        'ventas_hoy': ventas_hoy,
        'categorias': categorias,
        'proveedores': proveedores, 
        'remitos': remitos,  # <-- pasamos los remitos al template
        'query': query,
        'categoria_id': categoria_id
    }
    return render(request, 'dashboard.html', contexto)


def logoutView(request):
    logout(request)
    return redirect('home')  # Redirige al login después de cerrar sesión


def producto_lista(request):
    productos = Producto.objects.select_related('categoria', 'proveedor').all()
    return render(request, 'producto/producto_lista.html', {'productos': productos})


def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.activo = False
        producto.save()
        messages.success(request, "Producto desactivado correctamente.")
        return redirect('dashboard')
    return render(request, 'producto_confirmar_eliminar.html', {'producto': producto})


def producto_agregar(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('dashboard')
    else:
        form = ProductoForm()
    return render(request, 'producto/producto_agregar.html', {'form': form})

def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('dashboard')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'producto/producto_editar.html', {'form': form, 'producto': producto})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ClienteForm()

    return render(request, 'producto/crear_cliente.html', {
        'form': form,
        'titulo': 'Agregar Cliente'
    })


def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProveedorForm()

    return render(request, 'producto/crear_proveedor.html', {
        'form': form,
        'titulo': 'Agregar Proveedor'
    })

def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'producto/crear_categoria.html', {
        'form': form,
        'titulo': 'Crear categoría'
    })


# def crear_remito(request):
#     DetalleFormSet = inlineformset_factory(Remito, DetalleRemito, form=DetalleRemitoForm, extra=3)

#     if request.method == 'POST':
#         remito_form = RemitoForm(request.POST)
#         if remito_form.is_valid():
#             remito = remito_form.save(commit=False)
#             detalle_formset = DetalleFormSet(request.POST, instance=remito)

#             if detalle_formset.is_valid():
#                 with transaction.atomic():
#                     remito.save()
#                     detalles = detalle_formset.save(commit=False)
#                     total = 0
#                     for detalle in detalles:
#                         detalle.precio_unitario = detalle.producto.precio
#                         detalle.remito = remito
#                         detalle.save()
#                         total += detalle.subtotal()

#                     remito.importe_total = total
#                     remito.save()
#                 return redirect('dashboard')  # o a detalle_remito
#         else:
#             detalle_formset = DetalleFormSet(request.POST)
#     else:
#         remito_form = RemitoForm()
#         detalle_formset = DetalleFormSet()

#     return render(request, 'producto/crear_remito.html', {
#         'remito_form': remito_form,
#         'detalle_formset': detalle_formset
#     })


# def ver_Remito(request, remito_id):
#     remito = get_object_or_404(Remito, id=remito_id)
#     detalles = remito.detalles.all()
#     return render(request, "producto/ver_Remito.html", {"remito": remito, "detalles": detalles})

# Crear remito
def crear_remito(request):
    DetalleFormSet = modelformset_factory(DetalleRemito, form=DetalleRemitoForm, extra=1)
    
    if request.method == 'POST':
        remito_form = RemitoForm(request.POST)
        formset = DetalleFormSet(request.POST, queryset=DetalleRemito.objects.none())

        if remito_form.is_valid() and formset.is_valid():
            remito = remito_form.save(commit=False)
            remito.importe_total = 0
            remito.save()

            total = 0
            for detalle in formset:
                if detalle.cleaned_data:
                    detalle_instance = detalle.save(commit=False)
                    detalle_instance.remito = remito
                    detalle_instance.precio_unitario = detalle_instance.producto.precio
                    detalle_instance.save()
                    total += detalle_instance.subtotal()

            remito.importe_total = total
            remito.save()

            return redirect('ver_Remito', remito_id=remito.id)
    else:
        remito_form = RemitoForm()
        formset = DetalleFormSet(queryset=DetalleRemito.objects.none())

    return render(request, 'producto/crear_Remito.html', {'remito_form': remito_form, 'formset': formset})


# Ver remito
def ver_Remito(request, remito_id):
    remito = get_object_or_404(Remito, id=remito_id)
    detalles = remito.detalles.all()
    return render(request, 'producto/ver_Remito.html', {'remito': remito, 'detalles': detalles})
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

# def producto_eliminar(request, pk):
#     producto = get_object_or_404(Producto, pk=pk)
#     if request.method == 'POST':
#         producto.delete()
#         messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
#         return redirect('dashboard')  # o 'producto_lista' si tenés una vista separada
#     return render(request, 'producto/producto_eliminar.html', {'producto': producto})

# Create your views here.


# vista  basadas en funciones 
# def hola_mundo(request): 
#     return HttpResponse("hola mundo desde una vista basada en funciones")

# vista basadas en class
# class HolaMundoView(View):
#     def get(self,request): 
#         return HttpResponse("Hola Mundo desde una vista basada en clase")



# def dashboard(request):
#     # mensaje_compra = None
#     # mensaje_producto = None

#     # Formularios
#     compra_form = CompraForm()
#     producto_form = ProductoForm()

#     if request.method == 'POST':
#         if 'registrar_compra' in request.POST:
#             compra_form = CompraForm(request.POST)
#             if compra_form.is_valid():
#                 compra_form.save()
#                 messages.success(request, '¡Compra registrada!')
#                 return redirect('dashboard')
#         elif 'agregar_producto' in request.POST:
#             producto_form = ProductoForm(request.POST)
#             if producto_form.is_valid():
#                 producto_form.save()
#                 messages.success(request, '¡Producto creado exitosamente!')
#                 return redirect('dashboard')

#     # Filtros y métricas
#     query = request.GET.get('q', '').strip()
#     categoria_id = request.GET.get('categoria')
#     productos = Producto.objects.select_related('categoria', 'proveedor').filter(activo=True)

#     if query:
#         productos = productos.filter(nombre__icontains=query)
#     if categoria_id and categoria_id.isdigit():
#         productos = productos.filter(categoria_id=categoria_id)

#     total_productos = productos.count()
#     stock_bajo = productos.filter(stock__lte=F('stock_minimo')).count()
#     total_categorias = Categoria.objects.count()

#     contexto = {
#         'user': request.user,
#         'productos': productos,
#         'categorias': Categoria.objects.all(),
#         'total_productos': total_productos,
#         'stock_bajo': stock_bajo,
#         'total_categorias': total_categorias,
#         'ventas_hoy': 0,
#         'query': query,
#         'categoria_id': categoria_id,
#         'form': compra_form,
#         'producto_form': producto_form,
#     }

#     return render(request, 'dashboard.html', contexto)

# def dashboard(request):
#     compra_form = CompraForm()
#     producto_form = ProductoForm()

#     if request.method == 'POST':
#         if 'registrar_compra' in request.POST:
#             compra_form = CompraForm(request.POST)
#             if compra_form.is_valid():
#                 compra_form.save()
#                 messages.success(request, '¡Compra registrada!')
#                 return redirect('dashboard')

#         elif 'agregar_producto' in request.POST:
#             producto_form = ProductoForm(request.POST)
#             if producto_form.is_valid():
#                 producto_form.save()
#                 messages.success(request, '¡Producto creado exitosamente!')
#                 return redirect('dashboard')

#         elif 'eliminar_producto' in request.POST:
#             producto_id = request.POST.get('producto_id')
#             producto = get_object_or_404(Producto, pk=producto_id)
#             producto.delete()
#             messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
#             return redirect('dashboard')

#     # Filtros y métricas
#     query = request.GET.get('q', '').strip()
#     categoria_id = request.GET.get('categoria')
#     productos = Producto.objects.select_related('categoria', 'proveedor').filter(activo=True)

#     if query:
#         productos = productos.filter(nombre__icontains=query)
#     if categoria_id and categoria_id.isdigit():
#         productos = productos.filter(categoria_id=categoria_id)

#     total_productos = productos.count()
#     stock_bajo = productos.filter(stock__lte=F('stock_minimo')).count()
#     total_categorias = Categoria.objects.count()

#     contexto = {
#         'user': request.user,
#         'productos': productos,
#         'categorias': Categoria.objects.all(),
#         'total_productos': total_productos,
#         'stock_bajo': stock_bajo,
#         'total_categorias': total_categorias,
#         'ventas_hoy': 0,
#         'query': query,
#         'categoria_id': categoria_id,
#         'form': compra_form,
#         'producto_form': producto_form,
#     }

#     return render(request, 'dashboard.html', contexto)

# def index(request): 
#     auto = {'marca':'fiat', 'patente': 'afsg5757', 'modelo':'cronos' }
#     print(auto)
#     return render(request,"index.html", {"auto": auto})


# def loginView(request):
#     saludo = "BIENVENIDO A LA PÁGINA DE INICIO DE SESIÓN,POR FAVOR INGRESE SUS DATOS"
#     return render(request, "login.html", {'saludo': saludo})
