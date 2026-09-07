# Biblioteca App

Aplicacion academica de consola para practicar Programacion Orientada a Objetos, colecciones, relaciones entre objetos y persistencia basica con archivos JSON, y optimizacion de busquedas.

En este proyecto se puede observar como un programa puede mejorar su rendimiento cuando la cantidad de informacion empieza a crecer. La aplicacion sigue usando listas para conservar y guardar los datos, pero ahora crea indices internos con `dict` y `set` para acelerar busquedas, validaciones y consultas frecuentes.

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

## Mejora Semana 12: rendimiento con colecciones
Cuando trabajamos con pocos datos, recorrer una lista completa puede parecer suficiente. Sin embargo, en un sistema con miles de productos, clientes, pedidos o ventas, repetir recorridos lineales afecta el rendimiento, como en grandes cadenas de comida.

En esta refactorizacion se mantuvo el menu y las operaciones principales, pero se cambio la forma interna de consultar los datos. El sistema sigue cargando informacion desde archivos JSON hacia listas, y despues construye indices en memoria para responder mas rapido a las busquedas frecuentes.

Por eso, `RestauranteServicio` mantiene dos ideas al mismo tiempo:

- Listas (`list`) para conservar el orden, listar informacion y guardar nuevamente en JSON.
- Indices (`dict` y `set`) para buscar informacion de forma mas directa.

Ejemplos aplicados:

- `dict[str, Producto]`: permite buscar un producto por codigo sin recorrer toda la lista.
- `dict[str, Cliente]`: permite buscar un cliente por identificacion de forma directa.
- `dict[str, Prestamo]`: permite saber rapidamente si un producto tiene un pedido activo.
- `dict[str, list[Venta]]`: permite consultar ventas de un cliente sin revisar todas las ventas.
- `set[str]`: permite validar categorias unicas y consultar si una categoria existe.

Concepto aplicado: se usan estructuras de acceso directo. Una busqueda en lista necesita comparar elemento por elemento hasta encontrar el dato, por eso crece segun la cantidad de registros. En cambio, un diccionario usa una clave, como el codigo del libro o la identificacion del usuario, para llegar al dato de forma mucho mas rapida en promedio. El `set` aplica la misma idea para validar existencia sin recorrer manualmente todas las categorias.

La idea pedagogica es que el estudiante vea una refactorizacion interna: el menu no cambia, las operaciones siguen siendo las mismas, pero la forma de administrar los datos mejora pensando en escalabilidad.

## Operaciones principales

- Registrar, buscar, actualizar, eliminar y listar productos.
- Registrar, buscar, actualizar, eliminar y listar clientes.
- Prestar productos de tipo `PRESTAMO`.
- Devolver productos prestados.
- Vender productos de tipo `VENTA` y disminuir su stock.
- Consultar prestamos y ventas de un cliente.
- Listar categorias unicas usando `set`.
- Persistir toda la informacion en JSON.

## Ejecucion

Desde la carpeta `restaurante_app`, ejecutar:

```bash
python main.py
```

La aplicacion carga automaticamente los archivos de `datos/` al iniciar y guarda los cambios despues de cada operacion importante.
