import unittest
from carrito import Carrito

class TestCarrito(unittest.TestCase):

    def setUp(self):
        self.carrito = Carrito()

    # ── R1: AGREGAR PRODUCTOS ──────────────────────────
    def test_agregar_producto(self):
        self.carrito.agregar_producto("Camisa", 2, 50000)
        self.assertEqual(len(self.carrito.productos), 1)

    def test_agregar_producto_nombre(self):
        self.carrito.agregar_producto("Camisa", 2, 50000)
        self.assertEqual(self.carrito.productos[0]["nombre"], "Camisa")

    def test_agregar_varios_productos(self):
        self.carrito.agregar_producto("Camisa", 2, 50000)
        self.carrito.agregar_producto("Pantalon", 1, 80000)
        self.assertEqual(len(self.carrito.productos), 2)

    def test_cantidad_debe_ser_positiva(self):
        with self.assertRaises(ValueError):
            self.carrito.agregar_producto("Camisa", 0, 50000)

    def test_precio_debe_ser_positivo(self):
        with self.assertRaises(ValueError):
            self.carrito.agregar_producto("Camisa", 1, -1000)

    # ── R3: CALCULAR TOTAL ─────────────────────────────
    def test_total_carrito_vacio(self):
        self.assertEqual(self.carrito.calcular_total(), 0)

    def test_total_un_producto(self):
        self.carrito.agregar_producto("Camisa", 2, 50000)
        self.assertEqual(self.carrito.calcular_total(), 100000)

    def test_total_varios_productos(self):
        self.carrito.agregar_producto("Camisa", 2, 50000)
        self.carrito.agregar_producto("Pantalon", 1, 80000)
        self.assertEqual(self.carrito.calcular_total(), 180000)

    # ── R4: DESCUENTOS ─────────────────────────────────
    def test_descuento_porcentaje(self):
        self.carrito.agregar_producto("Camisa", 2, 50000)
        self.assertEqual(self.carrito.aplicar_descuento(porcentaje=10), 90000)

    def test_descuento_valor_fijo(self):
        self.carrito.agregar_producto("Camisa", 2, 50000)
        self.assertEqual(self.carrito.aplicar_descuento(valor_fijo=20000), 80000)

    def test_descuento_no_negativo(self):
        self.carrito.agregar_producto("Camisa", 1, 50000)
        self.assertEqual(self.carrito.aplicar_descuento(valor_fijo=200000), 0)

    def test_descuento_porcentaje_invalido(self):
        with self.assertRaises(ValueError):
            self.carrito.aplicar_descuento(porcentaje=110)

if __name__ == '__main__':
    unittest.main()