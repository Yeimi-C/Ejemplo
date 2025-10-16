from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
from typing import Optional


app = FastAPI(title="API de Productos")

# Modelo de entrada
class Product(BaseModel):
    id: int
    nombre: str
    categoria: str
    precio: float
    en_stock: bool

# Modelo de salida
class ProductOut(BaseModel):
    nombre: str
    categoria: str
    precio: float
    en_stock: bool

# "Base de datos" simulada
PRODUCT_DB: List[Product] = []

# Crear producto
@app.post("/productos", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: Product):
    for p in PRODUCT_DB:
        if p.id == producto.id:
            raise HTTPException(status_code=409, detail="El producto ya existe")
    PRODUCT_DB.append(producto)
    return producto

# Listar todos los productos
@app.get("/productos", response_model=List[ProductOut])
def listar_productos():
    return PRODUCT_DB

# Consultar producto por ID
@app.get("/productos/{id}", response_model=ProductOut)
def obtener_producto(id: int):
    for p in PRODUCT_DB:
        if p.id == id:
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Actualizar producto
@app.put("/productos/{id}", response_model=ProductOut)
def actualizar_producto(id: int, producto_actualizado: Product):
    for i, p in enumerate(PRODUCT_DB):
        if p.id == id:
            PRODUCT_DB[i] = producto_actualizado
            return producto_actualizado
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Eliminar producto
@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id: int):
    for i, p in enumerate(PRODUCT_DB):
        if p.id == id:
            del PRODUCT_DB[i]
            return
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/productos/filtro", response_model=List[ProductOut])
def filtrar_productos(categoria: Optional[str] = None, precio_max: Optional[float] = None):
    resultados = PRODUCT_DB

    if categoria:
        resultados = [p for p in resultados if p.categoria.lower() == categoria.lower()]
    if precio_max is not None:
        resultados = [p for p in resultados if p.precio <= precio_max]

    return resultados
