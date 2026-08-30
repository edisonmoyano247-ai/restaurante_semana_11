class Producto:
    # El producto ahora se diferencia si es para la venta en el local fisico o para un pedido en linea el que corre riesgo de ser devuelto.
    # El tipo permite explicar dos comportamientos distintos.
    # Pedido usa disponibilidad; VENTA usa stock.
    TIPO_PEDIDO = "PEDIDO"
    TIPO_VENTA = "VENTA"
    TIPOS_VALIDOS = (TIPO_PEDIDO, TIPO_VENTA)

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: str,
        categoria: str,
        tipo: str = TIPO_PEDIDO,
        disponible: bool = True,
        stock: int = 0,
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.tipo = tipo
        self.disponible = disponible
        self.stock = stock
        # Un producto para la venta en el local no se considera para pedido, por eso no usamos disponibilidad.
        if self.es_de_venta():
            self.disponible = False

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo no puede estar vacio.")
        self._codigo = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El campo nombre no puede estar vacio.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> str:
        return self._precio

    @precio.setter
    def precio(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El precio no puede estar vacio.")
        self._precio = valor.strip()

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La categoria no puede estar vacia.")
        self._categoria = valor.strip()

    @property
    def tipo(self) -> str:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El tipo no puede estar vacio.")

        tipo_normalizado = valor.strip().upper()
        if tipo_normalizado not in self.TIPOS_VALIDOS:
            raise ValueError("El tipo debe ser PEDIDO o VENTA.")

        self._tipo = tipo_normalizado

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            stock = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un numero entero.")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        self._stock = stock

    @property
    def estado(self) -> str:
        # El estado se muestra segun el tipo de producto.
        # Aqui se ve la diferencia pedagogica: venta muestra stock.
        if self.es_de_venta():
            return f"Stock: {self.stock}"
        # Pedido muestra disponibilidad.
        if self._disponible:
            return "Disponible"
        return "Pedido"

    def es_de_pedido(self) -> bool:
        return self.tipo == self.TIPO_PEDIDO

    def es_de_venta(self) -> bool:
        return self.tipo == self.TIPO_VENTA

    def pedir(self) -> bool:
        # Operacion de PEDIR: cambia disponible de True a False.
        if not self.es_de_pedido() or not self._disponible:
            return False
        self._disponible = False
        return True

    def cancelar(self) -> bool:
        # Operacion de CANCELAR: termina el pedido en line y vuelve disponible.
        if not self.es_de_pedido() or self._disponible:
            return False
        self._disponible = True
        return True

    def vender(self, cantidad: int = 1) -> bool:
        # Se agrega venta de productos mediante disminucion de stock.
        # Operacion de VENTA: no cambia disponibilidad, disminuye stock.
        if not self.es_de_venta():
            return False
        if cantidad <= 0 or self.stock < cantidad:
            return False

        self.stock -= cantidad
        return True

    def convertir_a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "tipo": self.tipo,
            "disponible": self.disponible,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return (
            f"Codigo: {self.codigo} | Nombre: {self.nombre} | "
            f"Precio: {self.precio} | Categoria: {self.categoria} | "
            f"Tipo: {self.tipo} | Estado: {self.estado}"
        )