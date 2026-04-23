from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, validator
from typing import List
from arbol import Nodo

app = FastAPI(
    title="Puzzle DFS",
    description="API para resolver un puzzle lineal de 4 elementos usando búsqueda en profundidad (DFS)",
    version="1.0.0"
)


class PuzzleRequest(BaseModel):
    estado_inicial: List[int]
    solucion: List[int]

    @validator("estado_inicial", "solucion")
    def validate_state(cls, v):
        if len(v) != 4:
            raise ValueError("El estado debe tener exactamente 4 elementos")
        if sorted(v) != [1, 2, 3, 4]:
            raise ValueError("El estado debe contener los números 1, 2, 3 y 4 sin repetir")
        return v


class PuzzleResponse(BaseModel):
    solucionado: bool
    pasos: List[List[int]]
    total_pasos: int
    mensaje: str


def buscar_solucion_DFS_rec(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())

    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    else:
        #Expandir nodos sucesores
        dato_nodo = nodo_inicial.get_datos()
        #Hijo izquierdo
        hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        hijo_izquierdo = Nodo(hijo)
        #Hijo Central
        hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        hijo_central = Nodo(hijo)
        #Hijo Derecho
        hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        hijo_derecho = Nodo(hijo)

        nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

    for nodo_hijo in nodo_inicial.get_hijos():
        if not nodo_hijo.get_datos() in visitados:
            # llamada recursiva
            sol = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados)
            if sol != None:
                return sol
            
    return None

def buscar_solucion_DFS(estado_inicial, solucion):
    visitados = []
    nodo_inicial = Nodo(estado_inicial)
    return buscar_solucion_DFS_rec(nodo_inicial, solucion, visitados)


@app.post("/api/resolver", response_model=PuzzleResponse)
def resolver_puzzle(request: PuzzleRequest):
    """Resuelve el puzzle lineal usando DFS."""
    if request.estado_inicial == request.solucion:
        return PuzzleResponse(
            solucionado=True,
            pasos=[request.estado_inicial],
            total_pasos=0,
            mensaje="El estado inicial ya es la solución"
        )

    nodo_solucion = buscar_solucion_DFS(request.estado_inicial, request.solucion)

    if nodo_solucion is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró solución dentro del límite de iteraciones"
        )

    # Reconstruir el camino
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(request.estado_inicial)
    resultado.reverse()

    return PuzzleResponse(
        solucionado=True,
        pasos=resultado,
        total_pasos=len(resultado) - 1,
        mensaje=f"Solución encontrada en {len(resultado) - 1} pasos"
    )


# Servir frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")
