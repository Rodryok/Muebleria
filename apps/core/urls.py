from django.urls import path
from . import views

urlpatterns = [

path('home/', views.home, name='home'),
path('login/', views.loginView, name='login'),
path('base/', views.base, name='base'),
path('dashboard/', views.dashboard, name='dashboard'),
path('logout/', views.logoutView, name='logout'),


# Rutas para gestionar productos
path('producto/agregar/', views.producto_agregar, name='producto_agregar'),
path('producto/editar/<int:pk>/', views.producto_editar, name='producto_editar'),
path('producto/eliminar/<int:pk>/', views.producto_eliminar, name='producto_eliminar'),
path('producto/lista/', views.producto_lista, name='producto_lista'),
path('producto/crear_remito/', views.crear_remito, name='crear_remito'),
path('producto/crear_cliente/', views.crear_cliente, name='crear_cliente'),
path('producto/crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
path('producto/crear_categoria/', views.crear_categoria, name='crear_categoria'),
path('producto/ver_Remito/<int:remito_id>/', views.ver_Remito, name='ver_Remito'),
]
