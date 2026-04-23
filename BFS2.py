from arbol import Nodo

def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    # Todo esto debe estar indentado (4 espacios o 1 Tab)
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)

    while not solucionado and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)    # Extraer el nodo y añadirlo a visitados
        
        if nodo.get_datos() == solucion:
            solucionado = True  # Solucion encontrada
            return nodo #Nodo solucion
        else:
            dato_nodo = nodo.get_datos()    # Expandir Nodos hijos
            hijo_izquierdo = Nodo(hijo) 
            


            # Obtenemos la lista de hijos (usamos get para evitar errores si no hay hijos)
            for un_hijo in conexiones.get(dato_nodo, []):   # Obtener izquierda de los nodos
                hijo = Nodo(un_hijo, nodo) 
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)
    return None
