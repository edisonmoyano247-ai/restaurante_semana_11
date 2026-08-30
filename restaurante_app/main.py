from pathlib import Path


from modelos.cliente import Cliente
from modelos.producto import Producto
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio

OPCIONES_MENU = (
    ("1", "Registrar producto"),
    ("2", "Buscar producto"),
    ("3", "Actualizar producto"),
    ("4", "Eliminar producto"),
    ("5", "Listar productos"),
    ("6", "Registrar cliente"),
    ("7", "Buscar cliente"),
    ("8", "Actualizar cliente"),
    ("9", "Eliminar cliente"),
    ("10", "Listar clientes"),
    ("11", "pedido producto"),
    ("12", "cancelar producto"),
    ("13", "Vender producto"),
    ("14", "Consultar operaciones de cliente"),
    ("15", "Listar categorias unicas"),
    ("0", "Salir"),
)


# Funciones pequenas para entrada por consola.
# La logica importante queda en RestauranteServicio.
def pedir_texto(mensaje: str) -> str:
    return input(mensaje).strip()


def pedir_entero(mensaje: str, valor_por_defecto: int | None = None) -> int:
    texto = pedir_texto(mensaje)
    if texto == "" and valor_por_defecto is not None:
        return valor_por_defecto
    return int(texto)


def mostrar_menu() -> None:
    print("\n===== RESTAURANTE APP =====")
    print("\nGESTION DE PRODUCTOS")
    for numero, descripcion in OPCIONES_MENU[:5]:
        print(f"{numero}. {descripcion}")

    print("\nGESTION DE USUARIOS")
    for numero, descripcion in OPCIONES_MENU[5:10]:
        print(f"{numero}. {descripcion}")

    print("\nOPERACIONES")
    for numero, descripcion in OPCIONES_MENU[10:14]:
        print(f"{numero}. {descripcion}")

    print("\nCONSULTAS")
    print(f"{OPCIONES_MENU[14][0]}. {OPCIONES_MENU[14][1]}")
    print("0. Salir")


def guardar_productos(archivo_servicio: ArchivoServicio, restaurante: RestauranteServicio) -> None:
    # Guardado automatico despues de modificar productos.
    guardado = archivo_servicio.guardar_productos(restaurante.listar_productos())
    if not guardado:
        print("Los cambios de productos no pudieron guardarse.")


def guardar_clientes(
    archivo_servicio: ArchivoServicio,
    restaurante: RestauranteServicio,
) -> None:
    # Guardado automatico despues de modificar clientes.
    guardado = archivo_servicio.guardar_clientes(restaurante.listar_clientes())
    if not guardado:
        print("Los cambios de clientes no pudieron guardarse.")


def guardar_pedidos(
    archivo_servicio: ArchivoServicio,
    restaurante: RestauranteServicio,
) -> None:
    # MEJORA SEMANA 11: los pedidos ahora se guardan en su propio JSON.
    # Guardado automatico despues de pedir o cancelar.
    guardado = archivo_servicio.guardar_pedidos(restaurante.listar_pedidos())
    if not guardado:
        print("Los cambios de pedidos no pudieron guardarse.")


def guardar_ventas(archivo_servicio: ArchivoServicio, restaurante: RestauranteServicio) -> None:
    # MEJORA SEMANA 11: las ventas ahora se guardan en su propio JSON.
    # Guardado automatico despues de vender.
    guardado = archivo_servicio.guardar_ventas(restaurante.listar_ventas())
    if not guardado:
        print("Los cambios de ventas no pudieron guardarse.")


def registrar_producto(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Registrar producto ---")
    codigo = pedir_texto("Codigo: ")
    nombre = pedir_texto("Nombre: ")
    precio = pedir_texto("Precio: ")
    categoria = pedir_texto("Categoria: ")
    tipo = pedir_texto("Tipo (PEDIDO/VENTA): ")

    try:
        stock = 0
        if tipo.strip().upper() == Producto.TIPO_VENTA:
            stock = pedir_entero("Stock: ")

        producto = Producto(codigo, nombre, precio, categoria, tipo, True, stock)
        registrado = restaurante.registrar_producto(producto)

        if registrado:
            print("Producto registrado correctamente.")
            guardar_productos(archivo_servicio, restaurante)
        else:
            print("El codigo ya se encuentra registrado.")
    except ValueError as error:
        print(error)


def buscar_producto(restaurante: RestauranteServicio) -> None:
    print("\n--- Buscar producto ---")
    codigo = pedir_texto("Codigo del producto: ")
    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
    else:
        print(producto)


def actualizar_producto(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Actualizar producto ---")
    codigo = pedir_texto("Codigo del producto: ")
    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
        return

    nuevo_nombre = pedir_texto("Nuevo nombre: ")
    nuevo_precio = pedir_texto("Nuevo precio: ")
    nueva_categoria = pedir_texto("Nueva categoria: ")
    nuevo_tipo = pedir_texto("Nuevo tipo (PEDIDO/VENTA): ")

    try:
        nuevo_stock = 0
        if nuevo_tipo.strip().upper() == Producto.TIPO_VENTA:
            nuevo_stock = pedir_entero("Nuevo stock: ")

        actualizado = restaurante.actualizar_producto(
            codigo,
            nuevo_nombre,
            nuevo_precio,
            nueva_categoria,
            nuevo_tipo,
            nuevo_stock,
        )

        if actualizado:
            print("Producto actualizado correctamente.")
            guardar_productos(archivo_servicio, restaurante)
        else:
            print("No se pudo actualizar. Revise si el producto tiene un pedido activo.")
    except ValueError as error:
        print(error)


def eliminar_producto(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio) -> None:
    print("\n--- Eliminar producto ---")
    codigo = pedir_texto("Codigo del producto: ")
    identificacion = restaurante.obtener_identificacion_pedido(codigo)

    if identificacion is not None:
        print(f"No se puede eliminar. El producto esta pedido al cliente {identificacion}.")
        return

    eliminado = restaurante.eliminar_producto(codigo)

    if eliminado:
        print("Producto eliminado correctamente.")
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("Producto no encontrado.")


def listar_productos(restaurante: RestauranteServicio) -> None:
    print("\n--- Lista de productos ---")
    productos = restaurante.listar_productos()

    if len(productos) == 0:
        print("No hay productos registrados.")
        return

    for indice, producto in enumerate(productos):
        print(f"{indice + 1}. {producto}")

    primer_producto = productos[0]
    print(f"\nPrimer producto registrado: {primer_producto.titulo}")
    print(f"Total de productos: {restaurante.contar_productos()}")


def registrar_cliente(
    restaurante: RestauranteServicio,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Registrar cliente ---")
    identificacion = pedir_texto("Identificacion: ")
    nombre = pedir_texto("Nombre: ")

    try:
        cliente = Cliente(identificacion, nombre)
        registrado = restaurante.registrar_cliente(cliente)

        if registrado:
            print("Cliente registrado correctamente.")
            guardar_clientes(archivo_servicio, restaurante)
        else:
            print("La identificacion ya se encuentra registrada.")
    except ValueError as error:
        print(error)


def buscar_cliente(restaurante: RestauranteServicio) -> None:
    print("\n--- Buscar cliente ---")
    identificacion = pedir_texto("Identificacion del cliente: ")
    cliente = restaurante.buscar_cliente(identificacion)

    if cliente is None:
        print("Cliente no encontrado.")
    else:
        print(cliente)


def actualizar_cliente(
    restaurante: RestauranteServicio,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Actualizar cliente ---")
    identificacion = pedir_texto("Identificacion del cliente: ")

    if restaurante.buscar_cliente(identificacion) is None:
        print("Cliente no encontrado.")
        return

    # CORRECCIÓN: Se cambió 'nuevo_precio' por 'nuevo_nombre'
    nuevo_nombre = pedir_texto("Nuevo nombre: ")

    try:
        actualizado = restaurante.actualizar_cliente(identificacion, nuevo_nombre)

        if actualizado:
            print("Cliente actualizado correctamente.")
            guardar_clientes(archivo_servicio, restaurante)
        else:
            print("Cliente no encontrado.")
    except ValueError as error:
        print(error)


def eliminar_cliente(
    restaurante: RestauranteServicio,
    archivo_servicio: ArchivoServicio,
) -> None:
    print("\n--- Eliminar cliente ---")
    identificacion = pedir_texto("Identificacion del cliente: ")
    eliminado = restaurante.eliminar_cliente(identificacion)

    if eliminado:
        print("Cliente eliminado correctamente.")
        guardar_clientes(archivo_servicio, restaurante)
    else:
        print("Cliente no encontrado o tiene pedidos activos.")


def listar_clientes(restaurante: RestauranteServicio) -> None:
    print("\n--- Lista de clientes ---")
    clientes = restaurante.listar_clientes()

    if len(clientes) == 0:
        print("No hay clientes registrados.")
        return

    for indice, cliente in enumerate(clientes):
        print(f"{indice + 1}. {cliente}")


def pedir_producto(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio) -> None:
    # MEJORA SEMANA 11: opcion del menu para crear un pedido.
    # Semana 11: desde esta opcion del menu se demuestra PEDIR.
    print("\n--- Pedir producto ---")
    codigo_producto = pedir_texto("Codigo del producto: ")
    identificacion_cliente = pedir_texto("Identificacion del cliente: ")

    # El main valida mensajes para el cliente, pero la regla final esta en el servicio.
    producto = restaurante.buscar_producto(codigo_producto)
    cliente = restaurante.buscar_cliente(identificacion_cliente)

    if cliente is None:
        print("Cliente no encontrado.")
        return
    if producto is None:
        print("Producto no encontrado.")
        return
    if not producto.es_de_pedido():
        print("No se puede pedir un producto de tipo VENTA.")
        return
    if not producto.disponible:
        print("El producto no esta disponible.")
        return

    pedido_realizado = restaurante.pedir_producto(codigo_producto, identificacion_cliente)
    if pedido_realizado:
        print(f"Producto pedido correctamente a {cliente.nombre}.")
        # Se guardan la nueva relacion y el cambio de disponibilidad del producto.
        guardar_pedidos(archivo_servicio, restaurante)
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("No fue posible realizar el pedido.")


def devolver_producto(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio) -> None:
    # MEJORA SEMANA 11: opcion del menu para cerrar un pedido.
    # Semana 11: desde esta opcion se demuestra CANCELAR/DEVOLVER.
    print("\n--- Devolver producto ---")
    codigo_producto = pedir_texto("Codigo del producto: ")
    identificacion_cliente = pedir_texto("Identificacion del cliente: ")

    devuelto = restaurante.devolver_producto(codigo_producto, identificacion_cliente)
    if devuelto:
        print("Producto devuelto correctamente.")
        # Se guarda el pedido finalizado y el producto disponible otra vez.
        guardar_pedidos(archivo_servicio, restaurante)
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("No se pudo devolver. Revise el producto, el cliente y el pedido activo.")


def vender_producto(restaurante: RestauranteServicio, archivo_servicio: ArchivoServicio) -> None:
    # MEJORA SEMANA 11: opcion del menu para registrar una venta.
    # Semana 11: desde esta opcion se demuestra VENDER.
    print("\n--- Vender producto ---")
    codigo_producto = pedir_texto("Codigo del producto: ")
    identificacion_cliente = pedir_texto("Identificacion del cliente: ")

    producto = restaurante.buscar_producto(codigo_producto)
    cliente = restaurante.buscar_cliente(identificacion_cliente)

    if cliente is None:
        print("Cliente no encontrado.")
        return
    if producto is None:
        print("Producto no encontrado.")
        return
    if not producto.es_de_venta():
        print("No se puede vender un producto de tipo PEDIDO.")
        return

    try:
        cantidad = pedir_entero("Cantidad (Enter para 1): ", 1)
        if producto.stock < cantidad:
            print("No hay stock suficiente.")
            return

        vendido = restaurante.vender_producto(codigo_producto, identificacion_cliente, cantidad)
        if vendido:
            print(f"Venta registrada correctamente. Stock actual: {producto.stock}")
            # Se guardan la venta creada y el nuevo stock del producto.
            guardar_ventas(archivo_servicio, restaurante)
            guardar_productos(archivo_servicio, restaurante)
        else:
            print("No fue posible realizar la venta.")
    except ValueError as error:
        print(error)


def consultar_operaciones_cliente(restaurante: RestauranteServicio) -> None:
    # MEJORA SEMANA 11: opcion del menu para ver relaciones de un cliente.
    # Semana 11: aqui se recorren relaciones ya creadas para un cliente.
    print("\n--- Operaciones de cliente ---")
    identificacion = pedir_texto("Identificacion del cliente: ")
    cliente = restaurante.buscar_cliente(identificacion)

    if cliente is None:
        print("Cliente no encontrado.")
        return

    pedidos, ventas = restaurante.consultar_operaciones_cliente(identificacion)
    print(f"\nCliente: {cliente.nombre}")

    print("\nPedidos:")
    if len(pedidos) == 0:
        print("- Sin pedidos activos")
    else:
        for pedido in pedidos:
            producto = restaurante.buscar_producto(pedido.producto_codigo)
            titulo = producto.titulo if producto is not None else "Producto no encontrado"
            print(f"- {pedido.producto_codigo} | {titulo}")

    print("\nVentas:")
    if len(ventas) == 0:
        print("- Sin ventas registradas")
    else:
        for venta in ventas:
            producto = restaurante.buscar_producto(venta.producto_codigo)
            titulo = producto.titulo if producto is not None else "Producto no encontrado"
            print(f"- {venta.producto_codigo} | {titulo} | Cantidad: {venta.cantidad}")


def listar_categorias_unicas(restaurante: RestauranteServicio) -> None:
    print("\n--- Categorias unicas ---")
    categorias = restaurante.obtener_categorias_unicas()

    if len(categorias) == 0:
        print("No hay categorias registradas.")
        return

    for categoria in sorted(categorias):
        print(f"- {categoria}")

    categoria_consultada = pedir_texto("\nConsultar si existe una categoria (Enter para omitir): ")
    if categoria_consultada:
        if restaurante.existe_categoria(categoria_consultada):
            print("La categoria existe en el restaurante.")
        else:
            print("La categoria no existe en el restaurante.")


def ejecutar_menu() -> None:
    ruta_datos = Path(__file__).resolve().parent / "datos"
    archivo_servicio = ArchivoServicio(str(ruta_datos))
    # MEJORA SEMANA 11: se restauran las cuatro colecciones al iniciar.
    # Al iniciar: JSON -> objetos -> colecciones dentro de RestauranteServicio.
    restaurante = RestauranteServicio(
        archivo_servicio.cargar_productos(),
        archivo_servicio.cargar_clientes(),
        archivo_servicio.cargar_pedidos(),
        archivo_servicio.cargar_ventas(),
    )

    guardar_productos(archivo_servicio, restaurante)

    opciones = {
        "1": lambda: registrar_producto(restaurante, archivo_servicio),
        "2": lambda: buscar_producto(restaurante),
        "3": lambda: actualizar_producto(restaurante, archivo_servicio),
        "4": lambda: eliminar_producto(restaurante, archivo_servicio),
        "5": lambda: listar_productos(restaurante),
        "6": lambda: registrar_cliente(restaurante, archivo_servicio),
        "7": lambda: buscar_cliente(restaurante),
        "8": lambda: actualizar_cliente(restaurante, archivo_servicio),
        "9": lambda: eliminar_cliente(restaurante, archivo_servicio),
        "10": lambda: listar_clientes(restaurante),
        "11": lambda: pedir_producto(restaurante, archivo_servicio),
        "12": lambda: devolver_producto(restaurante, archivo_servicio),
        "13": lambda: vender_producto(restaurante, archivo_servicio),
        "14": lambda: consultar_operaciones_cliente(restaurante),
        "15": lambda: listar_categorias_unicas(restaurante),
    }

    while True:
        mostrar_menu()
        opcion = pedir_texto("Seleccione una opcion: ")

        if opcion == "0":
            print("Gracias por usar Restaurante App.")
            break

        accion = opciones.get(opcion)
        if accion is None:
            print("Opcion invalida.")
        else:
            accion()


if __name__ == "__main__":
    ejecutar_menu()