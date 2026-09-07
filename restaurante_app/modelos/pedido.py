class Pedido:
    # MEJORA SEMANA 12: Mientras activo sea True, el libro esta prestado.
    def __init__(self, cliente_id: str, producto_codigo: str, activo: bool = True) -> None:
        self.cliente_id = cliente_id
        self.producto_codigo = producto_codigo
        self.activo = activo

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
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(self, valor: bool) -> None:
        self._activo = bool(valor)

    def finalizar(self) -> None:
        # Devolver un produto no borra la idea del pedido realizado; lo marca como cancelado.
        self.activo = False

    def convertir_a_diccionario(self) -> dict:
        return {
            "cliente_id": self.cliente_id,
            "producto_codigo": self.producto_codigo,
            "activo": self.activo,
        }

    def __str__(self) -> str:
        estado = "Activo" if self.activo else "Finalizado"
        return (
            f"Cliente: {self.cliente_id} | Producto: {self.producto_codigo} | "
            f"Estado: {estado}"
        )
