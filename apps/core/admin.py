from django.contrib import admin
from .models import Categoria, Proveedor, Cliente, Producto, Remito, DetalleRemito

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Remito)
admin.site.register(DetalleRemito)

