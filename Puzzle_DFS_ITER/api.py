from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from arbol import Nodo
from DFS_Iter import DFS_prof_iter

app = FastAPI(
    title="DFS Ciudades",
    description="API para resolver rutas entre ciudades usando búsqueda en profundidad iterativa (DFS)",
    version="1.0.0"
)

conexiones = {
    'EDO.MEX':{'QRO','SLP','SONORA'},
    'PUEBLA':{'HIDALGO','SLP'},
    'CDMX':{'MICHOACAN'},
    'MICHOACAN':{'SONORA'},
    'SLP':{'QRO','PUEBLA','EDO.MEX','SONORA'},
    'QRO':{'EDO.MEX','SLP'},
    'HIDALGO':{'PUEBLA','SONORA'},
    'MONTERREY':{'HIDALGO','SLP'},
    'SONORA':{'MONTERREY','HIDALGO','SLP','EDO.MEX','MICHOACAN'}
}

class CityRequest(BaseModel):
    estado_inicial: str
    solucion: str

class CityResponse(BaseModel):
    solucionado: bool
    pasos: List[str]
    total_pasos: int
    mensaje: str

@app.post("/api/resolver", response_model=CityResponse)
def resolver_puzzle(request: CityRequest):
    """Resuelve la ruta usando DFS iterativo."""
    if request.estado_inicial not in conexiones or request.solucion not in conexiones:
        raise HTTPException(
            status_code=400,
            detail="Ciudad no válida"
        )

    if request.estado_inicial == request.solucion:
        return CityResponse(
            solucionado=True,
            pasos=[request.estado_inicial],
            total_pasos=0,
            mensaje="El estado inicial ya es la solución"
        )

    nodo_inicial = Nodo(request.estado_inicial)
    nodo_solucion = DFS_prof_iter(nodo_inicial, request.solucion, conexiones)

    if nodo_solucion is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró ruta hacia la ciudad destino"
        )

    # Reconstruir el camino
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(request.estado_inicial)
    resultado.reverse()

    return CityResponse(
        solucionado=True,
        pasos=resultado,
        total_pasos=len(resultado) - 1,
        mensaje=f"Ruta encontrada en {len(resultado) - 1} pasos"
    )

# Servir frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")
