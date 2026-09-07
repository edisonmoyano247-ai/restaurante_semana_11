class Venta:
    # La cantidad permite explicar cuanto stock se descuenta.
    def __init__(self, cliente_id: str, producto_codigo: str, cantidad: int = 1) -> None:
        self.cliente_id = cliente_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    @property
    def cliente_id(self) -> str:
        return self._cliente_id

    @cliente_id.setter
    def cliente_id(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion del usuario no puede estar vacia.")
        self._cliente_id = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo del producto no puede estar vacio.")
        self._producto_codigo = valor.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        try:
            cantidad = int(valor)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un numero entero.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self._cantidad = cantidad

    def convertir_a_diccionario(self) -> dict:
        return {
            "cliente_id": self.cliente_id,
            "producto_codigo": self._producto_codigo,
            "cantidad": self.cantidad,
        }

    def __str__(self) -> str:
        return (
            f"Cliente: {self.cliente_id} | Producto: {self.producto_codigo} | "
            f"Cantidad: {self.cantidad}"
        )
