from django.core.exceptions import ValidationError
from django import forms
from .models import Cliente, Producto, Remito, DetalleRemito

#formulario para realizar compra
class CompraForm(forms.Form):
    nombre_cliente = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=200)
    producto_id = forms.IntegerField()
    cantidad = forms.IntegerField(min_value=1)

    #valida producto id
    def clean_producto_id(self):
        producto_id = self.cleaned_data['producto_id']
        
        if not Producto.objects.filter(id=producto_id).exists():
            raise ValidationError("El producto no existe.")
        return producto_id
    
    #valida cantidad y producto id
    def clean(self):
        cleaned_data = super().clean()
        producto_id = cleaned_data.get('producto_id')
        cantidad = cleaned_data.get('cantidad')

        if producto_id and cantidad:
            producto = Producto.objects.get(id=producto_id)
            if producto.stock < cantidad:
                raise ValidationError("Stock insuficiente.")
        return cleaned_data

    #almacena los valores para crear el remito y el detalleRemito
    def guardar(self):
        nombre = self.cleaned_data['nombre_cliente']
        direccion = self.cleaned_data['direccion']
        producto_id = self.cleaned_data['producto_id']
        cantidad = self.cleaned_data['cantidad']



        # busca o crea el cliente
        cliente, _ = Cliente.objects.get_or_create(
            nombre=nombre,
            direccion=direccion
        )

        # recupera el producto
        producto = Producto.objects.get(id=producto_id)
        # Calcular importe
        importe_total = producto.precio * cantidad

        # Crear remito
        remito = Remito.objects.create(
            cliente=cliente,
            importe_total=importe_total
        )

        # Crear detalleRemito
        DetalleRemito.objects.create(
            remito=remito,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            descripcion=f"Compra de {cantidad} unidad(es) de {producto.nombre}"
        )

        # Actualizar stock
        producto.stock -= cantidad
        producto.save()

        return remito
