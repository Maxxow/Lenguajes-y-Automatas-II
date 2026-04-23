#Viaje con carretera con busqueda de costo uniforme
from arbol import Nodo
def compara (x,y):
    return x.get_costo() -y.get_costo()

def buscar_solucion_UCS(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial.set_costo(0)
    nodos_frontera.append(nodo_inicial)
    while(not solucionado) and len(nodos_frontera) !=0:
        #Ordenar lista de nodos frontera
        nodos_frontera = sorted(nodos_frontera, cmp = compara)
        nodo = nodos_frontera[0]
        #Extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodos_frontera.pop(0))
        
    if nodo.get_datos() == solucion:
        solucionado = True
        return nodo
    else:
        dato_nodo=nodo.get_datos()
        lista_hijos = []
        for un_hijo in conexiones[dato_nodo]:
            hijo = Nodo(un_hijo)
            costo = conexiones[dato_nodo][un_hijo]
            hijo.set_costo(nodo.get_costo()+costo)
            lista_hijos.append(hijo)
            if not hijo.en_lista(nodos_visitados):
                #Si esta en la lista se sustituye con el nuevo valor del costosi es menor
                if hijo.en_lista(nodos_frontera):
                    for hijo in lista_hijos (nodos_frontera):
                        for n in nodos_frontera:
                            if n.igual(hijo) and n.get_costo()>hijo.get_costo():
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                            else:
                                nodos_frontera.append(hijo)
                                nodo.set_hijos(lista_hijos)

if __name__ == "__main__":
    conexiones = {
        'JILOYORK':{'CDMX':125, 'QRO':513},
        'MORELOS':{'QRO':524},
        'CDMX':{'JILOYORK':125, 'QRO':423, 'HGO':491},
        'HGO':{'CDMX':491, 'QRO':356, 'MEXICALI':109, 'MTY':348},
        'QRO':{'SLP':203, 'MORELOS':514, 'JILOYORK':513, 'CDMX':423, 'MTY':603, 'SONORA':437, 'HGO':356, 'MEXICALI':313, 'SONORA':437, 'AGS':599},
        'SLP':{'AGS':399, 'QRO':203},
        'AGS':{'SLP':390, 'QRO':203},
        'SONORA':{'QRO':437, 'MEXICALI':394},
        'MEXICALI':{'MTY':296, 'HGO':309,'QRO':313},
        'MTY':{'MEXICALI':524, 'QRO':603, 'HGO':346}
    }


                    