from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlalchemy as sa
import os

app = FastAPI(title="Carrito de Compras API")

# ── Conexion a la base de datos ────────────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"
)

engine = sa.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
metadata = sa.MetaData()

productos = sa.Table(
    "productos", metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("nombre", sa.String(100), nullable=False),
    sa.Column("cantidad", sa.Integer, nullable=False),
    sa.Column("precio", sa.Float, nullable=False),
)

metadata.create_all(engine)

# ── Modelos ────────────────────────────────────────
class ProductoIn(BaseModel):
    nombre: str
    cantidad: int
    precio: float

class ProductoOut(BaseModel):
    id: int
    nombre: str
    cantidad: int
    precio: float

# ── Endpoints ──────────────────────────────────────
@app.get("/")
def root():
    return {"mensaje": "API Carrito de Compras funcionando"}

@app.post("/productos", response_model=ProductoOut)
def crear_producto(producto: ProductoIn):
    if producto.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a cero")
    if producto.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor a cero")
    with engine.connect() as conn:
        result = conn.execute(
            productos.insert().values(
                nombre=producto.nombre,
                cantidad=producto.cantidad,
                precio=producto.precio
            )
        )
        conn.commit()
        id_nuevo = result.lastrowid
    return ProductoOut(id=id_nuevo, **producto.model_dump())

@app.get("/productos", response_model=List[ProductoOut])
def listar_productos():
    with engine.connect() as conn:
        result = conn.execute(productos.select())
        return [ProductoOut(**row._mapping) for row in result]

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            productos.delete().where(productos.c.id == producto_id)
        )
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": f"Producto {producto_id} eliminado"}

@app.get("/productos/{producto_id}", response_model=ProductoOut)
def obtener_producto(producto_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            productos.select().where(productos.c.id == producto_id)
        )
        row = result.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return ProductoOut(**row._mapping)