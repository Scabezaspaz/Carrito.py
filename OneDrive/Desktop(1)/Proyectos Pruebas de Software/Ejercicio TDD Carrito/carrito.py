class Carrito:
    """Carrito de compras con soporte para productos, totales y descuentos."""

    def __init__(self):
        self.productos = []

    # ── R1: AGREGAR PRODUCTOS ──────────────────────────────────────
    def agregar_producto(self, nombre: str, cantidad: int, precio: float) -> None:
        """Agrega un producto al carrito.

        Args:
            nombre: Nombre del producto.
            cantidad: Cantidad de unidades (debe ser mayor a 0).
            precio: Precio unitario (debe ser mayor a 0).

        Raises:
            ValueError: Si cantidad o precio son inválidos.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a cero")
        self.productos.append({
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio
        })

    # ── R3: CALCULAR TOTAL ─────────────────────────────────────────
    def calcular_total(self) -> float:
        """Retorna la suma de (precio × cantidad) de cada producto."""
        return sum(p["precio"] * p["cantidad"] for p in self.productos)

    # ── R4: APLICAR DESCUENTOS ─────────────────────────────────────
    def aplicar_descuento(self, porcentaje: float = 0, valor_fijo: float = 0) -> float:
        """Aplica un descuento al total del carrito.

        Args:
            porcentaje: Descuento en porcentaje (0-100).
            valor_fijo: Descuento en valor fijo.

        Returns:
            Total con descuento aplicado, mínimo 0.

        Raises:
            ValueError: Si el porcentaje está fuera del rango 0-100.
        """
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")

        total = self.calcular_total()

        if porcentaje:
            total = total - (total * porcentaje / 100)
        if valor_fijo:
            total = total - valor_fijo

        return max(0, total)