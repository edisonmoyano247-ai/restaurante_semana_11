# Biblioteca App

Aplicacion academica de consola para practicar Programacion Orientada a Objetos, colecciones, relaciones entre objetos y persistencia basica con archivos JSON.

EN la Semana 11 es observar como una coleccion de productos, una coleccion de clientes, una coleccion de pedidos y una coleccion de ventas permiten representar operaciones reales dentro del sistema.

## Estructura

```text
restaurante_app/
|
|-- datos/
|   |-- clientes.json
|   |-- pedidos.json
|   |-- productos.json
|   `-- ventas.json
|
|-- modelos/
|   |-- cliente.py
|   |-- pedido.py
|   |-- producto.py
|   `-- venta.py
|
|-- servicios/
|   |-- archivo_servicio.py
|   `-- restaurante_servicio.py
|
`-- main.py
```

- `modelos/`: clases principales del sistema y conversion a diccionario.
- `servicios/`: reglas de negocio y carga/guardado de archivos JSON.
- `datos/`: archivos JSON donde se conservan productos, clientes, pedidos y ventas.
- `main.py`: menu de consola y entrada de datos del usuario.

## Operaciones principales

- Registrar, buscar, actualizar, eliminar y listar productos.
- Registrar, buscar, actualizar, eliminar y listar clientes.
- Pedir productos de tipo `PRODUCTO`.
- Cancelar productos pedidos.
- Vender productos de tipo `VENTA` y disminuir su stock.
- Consultar pedidos y ventas de un cliente.
- Listar categorias unicas usando `set`.
- Persistir toda la informacion en JSON.

## Ejecucion

Desde la carpeta `restaurante_app`, ejecutar:

```bash
python main.py
```

La aplicacion carga automaticamente los archivos de `datos/` al iniciar y guarda los cambios despues de cada operacion importante.
