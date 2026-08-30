class Cliente:
    def __init__(self, identificacion: str, nombre: str) -> None:
        self.identificacion = identificacion
        self.nombre = nombre

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion no puede estar vacia.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacio.")
        self._nombre = valor.strip()

    def convertir_a_diccionario(self) -> dict:
        
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
        }

    def __str__(self) -> str:
        return f"Identificacion: {self.identificacion} | Nombre: {self.nombre}"
