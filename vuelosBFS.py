# Vuelos con busqueda en amplitud
from arbol import Nodo

def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while (not solucionado) and len(nodos_frontera) !=0:
        nodo = nodos_frontera.pop(0)
        #Extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            # solucion encontrada
            solucionado = True
            return nodo
        else:
            #Expandir los nodos hijo (ciudades con conexion)
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones(dato_nodo):
                hijo = Nodo(un_hijo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)

            nodo.set_hijos(lista_hijos)

if __name__ == "__main__":
    conexiones = {
        'Jiloyork': {'Celaya', 'CDMX', 'Queretaro'},
        'Sonora':{'Zacatecas','Sinaloa'},
        'Guanajuato':{'Aguascalientes'},
        'Oaxaca':{'Queretaro'},
        'Sinaloa':{'Celaya', 'Sonora', 'Jiloyork'},
        'Queretaro':{'Monterrey'},
        'Celaya':{'Jiloyork', 'Sinaloa'},
        'Zacatecas':{'Sonora', 'Monterrey', 'Queretaro'},
        'Monterrey':{'Zacatecas','Sinaloa'},
        'Tamaulipas':{'Queretaro'},
        'CDMX':{'Tamaulipas', 'Zacatecas', 'Sinaloa', 'Jiloyork', 'Oaxaca'},
    }

    estado_inicial = 'Jiloyork'
    solucion = 'Zacatecas'
    nodo_solucion = buscar_solucion_BFS(conexiones, estado_inicial, solucion)
    # Nota: Rcordar estudiar de nuevo esto con los archivos que ya teniamos antes
    # Mostrar Resultado
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() != None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()
    print (resultado)