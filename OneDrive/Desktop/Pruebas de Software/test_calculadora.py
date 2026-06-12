import unittest
from calculadora import Calculadora

class TestCalculadora(unittest.TestCase):

    def test_suma(self):
        calc = Calculadora()
        resultado = calc.sumar(5, 3)
        self.assertEqual(resultado, 8)

if __name__ == '__main__':
    unittest.main()