# Create your models here.
from django.db import models

# Productos, Proveedores, Clientes, Remitos y Detalles de Remitos


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # return f"La categoria es {self.nombre}" 
        return self.nombre
    


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)


    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField()
    stock_minimo = 0
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/',default='productos/default.jpg')
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="productos"
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.PROTECT, related_name="productos"
    )

    def __str__(self):
        return f"{self.nombre} (${self.precio})"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


    def __str__(self):
        return self.nombre


class Remito(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="remitos"
    )
    fecha = models.DateField(auto_now_add=True)
    importe_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Remito #{self.id} - {self.cliente.nombre} ({self.fecha})"


class DetalleRemito(models.Model):
    remito = models.ForeignKey(
        Remito, on_delete=models.CASCADE, related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.PROTECT, related_name="detalles"
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"
    


# class productoImagen(models.Model):
#     producto = models.ForeignKey(
#         Producto, on_delete=models.CASCADE, related_name="imagenes"
#     )
#     descripcion = models.TextField(blank=True, null=True)
#     avatar = models.ImageField(upload_to='productos/',default='productos/default.jpg')
#     def __str__(self):
#         return f"Imagen de {self.producto.nombre}"