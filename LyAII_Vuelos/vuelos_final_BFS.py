from arbol import Nodo

def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = [] 
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)
    while (not solucionado) and len(nodos_frontera)!=0:
        nodo = nodos_frontera.pop(0)
        # Extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            # Solución encontrada
            solucionado = True
            return nodo
        else:
            # Expandir los nodos hijo
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados)\
                    and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)
            nodo.set_hijos(lista_hijos)

if __name__ == "__main__":
    conexiones = {
        'JILOYORK': {'CELAYA', 'CDMX', 'QUERETARO', 'SINALOA'},
        'SONORA': {'ZACATECAS', 'SINALOA'},
        'GUANAJUATO': {'AGUASCALIENTES', 'CELAYA'},
        'AGUASCALIENTES': {'GUANAJUATO', 'ZACATECAS'},
        'OAXACA': {'QUERETARO', 'CDMX'},
        'SINALOA': {'CELAYA', 'SONORA', 'JILOYORK', 'MONTERREY', 'CDMX'},
        'QUERETARO': {'MONTERREY', 'JILOYORK', 'OAXACA', 'ZACATECAS', 'TAMAULIPAS'},
        'CELAYA': {'JILOYORK', 'SINALOA', 'GUANAJUATO'},
        'ZACATECAS': {'SONORA', 'MONTERREY', 'QUERETARO', 'CDMX', 'AGUASCALIENTES'},
        'MONTERREY': {'ZACATECAS', 'SINALOA', 'QUERETARO'},
        'TAMAULIPAS': {'QUERETARO', 'CDMX'},
        'CDMX': {'TAMAULIPAS', 'ZACATECAS', 'SINALOA', 'JILOYORK', 'OAXACA'}
    }

    print("--- INICIANDO BÚSQUEDA DE RUTAS ---")
    estado_inicial = input("Ingresa el estado inicial (o 'salir' para terminar): ").strip().upper()

    while estado_inicial != 'SALIR':
        if estado_inicial not in conexiones:
            print(f"El estado {estado_inicial} no existe en las conexiones.")
            estado_inicial = input("Ingresa un estado inicial válido (o 'salir' para terminar): ").strip().upper()
            continue

        solucion = input(f"Te encuentras en {estado_inicial}. Ingresa el destino (o 'salir' para terminar): ").strip().upper()
        
        if solucion == 'SALIR':
            print("Saliendo del programa...")
            break
            
        if solucion not in conexiones:
            print(f"El destino {solucion} no existe en las conexiones.")
            continue

        if estado_inicial == solucion:
            print(f"Ya te encuentras en {solucion}.")
            continue

        nodo_solucion = buscar_solucion_BFS(conexiones, estado_inicial, solucion)

        if nodo_solucion is None:
            print(f"No se encontró ninguna ruta desde {estado_inicial} a {solucion}.")
        else:
            # Mostrar Resultado
            resultado = []
            nodo = nodo_solucion
            while nodo.get_padre() is not None:
                resultado.append(nodo.get_datos())
                nodo = nodo.get_padre()
            resultado.append(estado_inicial)
            resultado.reverse()
            print("Ruta: " + " -> ".join(resultado))
            
            # Convertir solución en nuevo estado inicial
            estado_inicial = solucion
            print(f"\n¡Has llegado a {estado_inicial}! Ahora es tu nuevo punto de partida.")
