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
        # Estas listas permiten explicar recorrido, busqueda y relaciones.
        self._productos: list[Producto] = productos_iniciales.copy() if productos_iniciales else []
        self._clientes: list[Cliente] = (
            clientes_iniciales.copy() if clientes_iniciales else []
        )
        self._pedidos: list[Pedido] = (
            pedidos_iniciales.copy() if pedidos_iniciales else []
        )
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []

        # MEJORA SEMANA 12: indices internos para optimizar busquedas.
        # Las listas se mantienen para listar y guardar en JSON, pero los diccionarios
        # permiten encontrar libros, usuarios y prestamos sin recorrer toda la coleccion.
        self._productos_por_codigo: dict[str, Producto] = {}
        self._clientes_por_identificacion: dict[str, Cliente] = {}
        self._pedidos_activos_por_producto: dict[str, Pedido] = {}
        self._pedidos_activos_por_cliente: dict[str, list[Pedido]] = {}
        self._ventas_por_cliente: dict[str, list[Venta]] = {}
        self._categorias: set[str] = set()

        self._reconstruir_indices()
        self.sincronizar_estado_pedidos()

    def _reconstruir_indices(self) -> None:
        # MEJORA SEMANA 12: al cargar datos desde JSON llegan como listas.
        # Aqui se crean estructuras auxiliares en memoria para acelerar consultas.
        self._productos_por_codigo = {}
        self._clientes_por_identificacion = {}
        self._pedidos_activos_por_producto = {}
        self._pedidos_activos_por_cliente = {}
        self._ventas_por_cliente = {}
        self._categorias = set()
        
        for producto in self._productos:
            self._productos_por_codigo[producto.codigo] = producto
            self._categorias.add(producto.categoria)

        for cliente in self._clientes:
            self._clientes_por_identificacion[cliente.identificacion] = cliente

        for pedido in self._pedidos:
            if pedido.activo:
                self._registrar_indice_pedido_activo(pedido)

        for venta in self._ventas:
            self._ventas_por_cliente.setdefault(venta.cliente_id, []).append(venta)

    def _registrar_indice_pedido_activo(self, pedido: Pedido) -> None:
        self._pedidos_activos_por_producto[pedido.producto_codigo] = pedido
        self._pedidos_activos_por_cliente.setdefault(
            pedido.cliente_id,
            [],
        ).append(pedido)

    def _quitar_indice_pedido_activo(self, pedido: Pedido) -> None:
        self._pedidos_activos_por_producto.pop(pedido.producto_codigo, None)

        pedidos_cliente = self._pedidos_activos_por_cliente.get(pedido.cliente_id)
        if pedidos_cliente is None:
            return

        if pedido in pedidos_cliente:
            pedidos_cliente.remove(pedido)

        if len(pedidos_cliente) == 0:
            self._pedidos_activos_por_cliente.pop(pedido.cliente_id, None)

    def _reconstruir_indice_categorias(self) -> None:
        self._categorias = {producto.categoria for producto in self._productos}

    def sincronizar_estado_pedidos(self) -> None:
        # Al cargar desde JSON, primero todos los productos de pedidos quedan libres.
        for producto in self._productos:
            if producto.es_de_pedido():
                producto.disponible = True

        # Luego cada pedido activo vuelve a marcar su producto como no disponible.
        for pedido in self._pedidos:
            if pedido.activo:
                # MEJORA SEMANA 12: buscar_pedido usa el indice por codigo.
                producto = self.buscar_producto(pedido.producto_codigo)
                if producto is not None and producto.es_de_pedido():
                    producto.disponible = False

    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo) is not None:
            return False

        self._productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        self._categorias.add(producto.categoria)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        # MEJORA SEMANA 12: busqueda directa por clave.
        # Antes se recorria toda la lista de productos. Con dict, el acceso promedio es O(1).
        codigo = codigo.strip()
        return self._productos_por_codigo.get(codigo)      

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
        self._reconstruir_indice_categorias()            
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        if self.buscar_pedido_activo(codigo) is not None:
            return False

        self._productos.remove(producto)
        self._productos_por_codigo.pop(producto.codigo, None)
        self._reconstruir_indice_categorias()
        return True

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def contar_productos(self) -> int:
        return len(self._productos)

    def registrar_cliente(self, cliente: Cliente) -> bool:
        if self.buscar_cliente(cliente.identificacion) is not None:
            return False

        self._clientes.append(cliente)
        self._clientes_por_identificacion[cliente.identificacion] = cliente
        return True

    def buscar_cliente(self, identificacion: str) -> Cliente | None:
        # MEJORA SEMANA 12: busqueda optimizada por identificacion.
        # En un sistema con miles de usuarios evitamos recorrer la lista completa.
        identificacion = identificacion.strip()
        return self._clientes_por_identificacion.get(identificacion)

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
        self._clientes_por_identificacion.pop(cliente.identificacion, None)
        return True    

    def listar_clientes(self) -> list[Cliente]:
        return self._clientes.copy()

    def pedir_producto(self, codigo_producto: str, identificacion_cliente: str) -> bool:
        # Se incluye operacion para prestar y relacionar cliente-producto.
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
        self._registrar_indice_pedido_activo(pedido)
        # Y aqui se ve el cambio interno del producto: disponible True -> False.
        producto.pedir()
        return True

    def devolver_producto(self, codigo_producto: str, identificacion_cliente: str) -> bool:
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
        self._quitar_indice_pedido_activo(pedido)
        # Y el producto vuelve a estar disponible.
        producto.cancelar()
        return True

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_cliente: str,
        cantidad: int = 1,
    ) -> bool:
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
        self._ventas_por_cliente.setdefault(cliente.identificacion, []).append(venta)
        # Y aqui se ve el cambio interno del producto: stock disminuye.
        producto.vender(cantidad)
        return True

    def buscar_pedido_activo(self, codigo_producto: str) -> Pedido | None:
        # MEJORA SEMANA 12: indice de pedidos activos por codigo de producto.
        # Antes se recorria la lista de pedidos. Ahora se consulta un dict.
        codigo_producto = codigo_producto.strip()
        return self._pedidos_activos_por_producto.get(codigo_producto)    

    def cliente_tiene_pedidos_activos(self, identificacion: str) -> bool:
        # MEJORA SEMANA 12: verificar existencia en dict evita filtrar todos los pedidos.
        identificacion = identificacion.strip()
        return identificacion in self._pedidos_activos_por_cliente

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
        # MEJORA SEMANA 12: consulta optimizada por usuario.
        # En lugar de recorrer prestamos y ventas completos, usamos indices por usuario.
        identificacion_cliente = identificacion_cliente.strip()
        pedidos_cliente = self._pedidos_activos_por_cliente.get(
            identificacion_cliente,
            [],
        )
        ventas_cliente = self._ventas_por_cliente.get(identificacion_cliente, [])
        return pedidos_cliente.copy(), ventas_cliente.copy()

    def obtener_categorias_unicas(self) -> set[str]:
        # MEJORA SEMANA 12: las categorias se mantienen en un set actualizado.
        # Asi evitamos reconstruirlo cada vez que se consulta.
        return self._categorias.copy()

    def existe_categoria(self, categoria: str) -> bool:
        # MEJORA SEMANA 12: pertenencia en set, ideal para validaciones rapidas.
        return categoria.strip() in self._categorias
