import pytest
from carrito import Carrito
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ── Tests del Carrito (logica de negocio) ──────────
@pytest.fixture
def carrito():
    return Carrito()

def test_agregar_producto(carrito):
    carrito.agregar_producto("Camisa", 2, 50000)
    assert len(carrito.productos) == 1

def test_agregar_producto_nombre(carrito):
    carrito.agregar_producto("Camisa", 2, 50000)
    assert carrito.productos[0]["nombre"] == "Camisa"

def test_agregar_varios_productos(carrito):
    carrito.agregar_producto("Camisa", 2, 50000)
    carrito.agregar_producto("Pantalon", 1, 80000)
    assert len(carrito.productos) == 2

def test_cantidad_debe_ser_positiva(carrito):
    with pytest.raises(ValueError):
        carrito.agregar_producto("Camisa", 0, 50000)

def test_precio_debe_ser_positivo(carrito):
    with pytest.raises(ValueError):
        carrito.agregar_producto("Camisa", 1, -1000)

def test_total_carrito_vacio(carrito):
    assert carrito.calcular_total() == 0

def test_total_un_producto(carrito):
    carrito.agregar_producto("Camisa", 2, 50000)
    assert carrito.calcular_total() == 100000

def test_total_varios_productos(carrito):
    carrito.agregar_producto("Camisa", 2, 50000)
    carrito.agregar_producto("Pantalon", 1, 80000)
    assert carrito.calcular_total() == 180000

def test_descuento_porcentaje(carrito):
    carrito.agregar_producto("Camisa", 2, 50000)
    assert carrito.aplicar_descuento(porcentaje=10) == 90000

def test_descuento_valor_fijo(carrito):
    carrito.agregar_producto("Camisa", 2, 50000)
    assert carrito.aplicar_descuento(valor_fijo=20000) == 80000

def test_descuento_no_negativo(carrito):
    carrito.agregar_producto("Camisa", 1, 50000)
    assert carrito.aplicar_descuento(valor_fijo=200000) == 0

def test_descuento_porcentaje_invalido(carrito):
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(porcentaje=110)

# ── Tests de la API ────────────────────────────────
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "API Carrito de Compras funcionando"

def test_crear_producto_api():
    response = client.post("/productos", json={
        "nombre": "Camisa",
        "cantidad": 2,
        "precio": 50000
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Camisa"

def test_listar_productos_api():
    response = client.get("/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_producto_cantidad_invalida():
    response = client.post("/productos", json={
        "nombre": "Camisa",
        "cantidad": 0,
        "precio": 50000
    })
    assert response.status_code == 400

def test_obtener_producto_api():
    client.post("/productos", json={
        "nombre": "Zapatos",
        "cantidad": 1,
        "precio": 120000
    })
    response = client.get("/productos/1")
    assert response.status_code == 200