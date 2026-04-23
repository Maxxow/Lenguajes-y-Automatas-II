from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from BFS import buscar_solucion_BFS

app = FastAPI()

class PuzzleRequest(BaseModel):
    estado_inicial: List[int]
    solucion: List[int]

@app.post("/api/solve")
async def solve_puzzle(req: PuzzleRequest):
    if len(req.estado_inicial) != 4 or len(req.solucion) != 4:
        raise HTTPException(status_code=400, detail="Los estados deben tener exactamente 4 elementos")
    
    nodo_solucion = buscar_solucion_BFS(req.estado_inicial, req.solucion)
    
    if nodo_solucion is not None:
        resultado = []
        nodo = nodo_solucion
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.append(req.estado_inicial)
        resultado.reverse()
        return {"success": True, "path": resultado}
    else:
        return {"success": False, "message": "No se encontró solución"}

# Mount the static files (the frontend)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
