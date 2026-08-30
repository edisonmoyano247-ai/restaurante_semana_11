from modelos.producto import Producto
from modelos.pedido import Pedido
from modelos.cliente import Cliente
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(
        self,
        productos_iniciales: list[Producto] | None = None,
        clientes_iniciales: list[Cliente] | None = None,
        pedidos_iniciales: list[Pedido] | None = None,
        ventas_iniciales: list[Venta] | None = None,
    ) -> None:
        # El servicio administra cuatro colecciones relacionadas.
        # Cuatro colecciones principales del sistema.
        # Estas listas permiten explicar recorrido, busqueda y relaciones.
        self._productos: list[Producto] = productos_iniciales.copy() if productos_iniciales else []
        self._clientes: list[Cliente] = (
            clientes_iniciales.copy() if clientes_iniciales else []
        )
        self._pedidos: list[Pedido] = (
            pedidos_iniciales.copy() if pedidos_iniciales else []
        )
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []
        self.sincronizar_estado_pedidos()

    def sincronizar_estado_pedidos(self) -> None:
        # Al cargar pedidos activos se reconstruye el estado real.
        # Al cargar desde JSON, primero todos los productos de prestamo quedan libres.
        for producto in self._productos:
            if producto.es_de_pedido():
                producto.disponible = True

        # Luego cada pedido activo vuelve a marcar su producto como no disponible.
        for pedido in self._pedidos:
            if pedido.activo:
                producto = self.buscar_producto(pedido.producto_codigo)
                if producto is not None and producto.es_de_pedido():
                    producto.disponible = False

    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo) is not None:
            return False

        self._productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo = codigo.strip()
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: str,
        nuevo_precio: str,
        nueva_categoria: str,
        nuevo_tipo: str,
        nuevo_stock: int,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False

        # No cambiamos a VENTA un producto que todavia tiene un pedido activo.
        tipo_normalizado = nuevo_tipo.strip().upper()
        if (
            self.buscar_pedido_activo(codigo) is not None
            and tipo_normalizado != Producto.TIPO_PEDIDO
        ):
            return False

        producto.nombre = nuevo_nombre
        producto.precio = nuevo_precio
        producto.categoria = nueva_categoria
        producto.tipo = nuevo_tipo
        producto.stock = nuevo_stock
        if producto.es_de_venta():
            producto.disponible = False
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        if self.buscar_pedido_activo(codigo) is not None:
            return False

        self._productos.remove(producto)
        return True

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def contar_productos(self) -> int:
        return len(self._productos)

    def registrar_cliente(self, cliente: Cliente) -> bool:
        if self.buscar_cliente(cliente.identificacion) is not None:
            return False

        self._clientes.append(cliente)
        return True

    def buscar_cliente(self, identificacion: str) -> Cliente | None:
        identificacion = identificacion.strip()
        for cliente in self._clientes:
            if cliente.identificacion == identificacion:
                return cliente
        return None

    def actualizar_cliente(self, identificacion: str, nuevo_nombre: str) -> bool:
        cliente = self.buscar_cliente(identificacion)
        if cliente is None:
            return False

        cliente.nombre = nuevo_nombre
        return True

    def eliminar_cliente(self, identificacion: str) -> bool:
        cliente = self.buscar_cliente(identificacion)
        if cliente is None:
            return False
        if self.cliente_tiene_pedidos_activos(identificacion):
            return False

        self._clientes.remove(cliente)
        return True

    def listar_clientes(self) -> list[Cliente]:
        return self._clientes.copy()

    def pedir_producto(self, codigo_producto: str, identificacion_cliente: str) -> bool:
        # Se incluye operacion para prestar y relacionar cliente-producto.
        # Desde aqui empieza la operacion central: Cliente -> Pedido -> Producto.
        cliente = self.buscar_cliente(identificacion_cliente)
        producto = self.buscar_producto(codigo_producto)

        # Reglas de negocio antes de crear la relacion.
        if cliente is None or producto is None:
            return False
        if not producto.es_de_pedido():
            return False
        if not producto.disponible:
            return False
        if self.buscar_pedido_activo(producto.codigo) is not None:
            return False

        # Aqui se crea la relacion entre cliente y producto.
        pedido = Pedido(cliente.identificacion, producto.codigo)
        self._pedidos.append(pedido)
        # Y aqui se ve el cambio interno del producto: disponible True -> False.
        producto.pedir()
        return True

    def devolver_producto(self, codigo_producto: str, identificacion_cliente: str) -> bool:
        # Se incluye una nueva operacion para finalizar un prestamo activo.
        # Devolver busca la relacion activa que se habia creado al pedir.
        pedido = self.buscar_pedido_activo(codigo_producto)
        producto = self.buscar_producto(codigo_producto)

        if pedido is None or producto is None:
            return False
        if pedido.cliente_id != identificacion_cliente.strip():
            return False
        if producto.disponible:
            return False

        # Aqui termina la relacion activa.
        pedido.finalizar()
        # Y el producto vuelve a estar disponible.
        producto.cancelar()
        return True

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_cliente: str,
        cantidad: int = 1,
    ) -> bool:
        # MEJORA SEMANA 11: nueva operacion para vender y descontar stock.
        # Desde aqui empieza la operacion de venta: Cliente -> Venta -> Producto.
        cliente = self.buscar_cliente(identificacion_cliente)
        producto = self.buscar_producto(codigo_producto)

        # Reglas de negocio: cliente, producto, tipo VENTA y stock suficiente.
        if cliente is None or producto is None:
            return False
        if not producto.es_de_venta():
            return False
        if producto.stock < cantidad:
            return False

        # Aqui se registra la relacion de venta.
        venta = Venta(cliente.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        # Y aqui se ve el cambio interno del producto: stock disminuye.
        producto.vender(cantidad)
        return True

    def buscar_pedido_activo(self, codigo_producto: str) -> Pedido | None:
        # MEJORA SEMANA 11: se busca en la coleccion de prestamos, no en un dict simple.
        # Busqueda en la coleccion de prestamos para saber si un producto esta ocupado.
        codigo_producto = codigo_producto.strip()
        for pedido in self._pedidos:
            if pedido.producto_codigo == codigo_producto and pedido.activo:
                return pedido
        return None

    def cliente_tiene_pedidos_activos(self, identificacion: str) -> bool:
        identificacion = identificacion.strip()
        for pedido in self._pedidos:
            if pedido.cliente_id == identificacion and pedido.activo:
                return True
        return False

    def obtener_identificacion_pedido(self, codigo_producto: str) -> str | None:
        pedido = self.buscar_pedido_activo(codigo_producto)
        if pedido is None:
            return None
        return pedido.cliente_id

    def listar_pedidos(self) -> list[Pedido]:
        return self._pedidos.copy()

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def consultar_operaciones_cliente(
        self,
        identificacion_cliente: str,
    ) -> tuple[list[Pedido], list[Venta]]:
        # MEJORA SEMANA 11: consulta relaciones de prestamos y ventas por cliente.
        # Consulta pedagogica: filtrar dos colecciones usando el id del cliente.
        identificacion_cliente = identificacion_cliente.strip()
        pedidos_cliente: list[Pedido] = []
        ventas_cliente: list[Venta] = []

        for pedido in self._pedidos:
            if pedido.cliente_id == identificacion_cliente and pedido.activo:
                pedidos_cliente.append(pedido)

        for venta in self._ventas:
            if venta.cliente_id == identificacion_cliente:
                ventas_cliente.append(venta)

        return pedidos_cliente, ventas_cliente

    def obtener_categorias_unicas(self) -> set[str]:
        categorias: set[str] = set()
        for producto in self._productos:
            categorias.add(producto.categoria)
        return categorias

    def existe_categoria(self, categoria: str) -> bool:
        return categoria.strip() in self.obtener_categorias_unicas()