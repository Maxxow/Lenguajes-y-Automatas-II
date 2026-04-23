import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from arbol import Nodo

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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


def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)
    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados) \
                        and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)
            nodo.set_hijos(lista_hijos)
    return None


@app.route('/api/ciudades', methods=['GET'])
def get_ciudades():
    """Retorna la lista de ciudades disponibles."""
    ciudades = sorted(list(conexiones.keys()))
    return jsonify({'ciudades': ciudades})


@app.route('/api/conexiones/<ciudad>', methods=['GET'])
def get_conexiones(ciudad):
    """Retorna las conexiones directas de una ciudad."""
    ciudad = ciudad.upper()
    if ciudad not in conexiones:
        return jsonify({'error': f'Ciudad {ciudad} no encontrada'}), 404
    return jsonify({
        'ciudad': ciudad,
        'conexiones': sorted(list(conexiones[ciudad]))
    })


@app.route('/api/buscar', methods=['POST'])
def buscar_ruta():
    """Busca una ruta entre origen y destino usando BFS."""
    data = request.get_json()
    origen = data.get('origen', '').strip().upper()
    destino = data.get('destino', '').strip().upper()

    if not origen or not destino:
        return jsonify({'error': 'Se requieren origen y destino'}), 400

    if origen not in conexiones:
        return jsonify({'error': f'Ciudad de origen "{origen}" no existe'}), 404

    if destino not in conexiones:
        return jsonify({'error': f'Ciudad de destino "{destino}" no existe'}), 404

    if origen == destino:
        return jsonify({
            'ruta': [origen],
            'mensaje': f'Ya te encuentras en {origen}',
            'destino_final': origen
        })

    nodo_solucion = buscar_solucion_BFS(conexiones, origen, destino)

    if nodo_solucion is None:
        return jsonify({
            'error': f'No se encontró ruta de {origen} a {destino}'
        }), 404

    # Reconstruir la ruta
    resultado = []
    nodo = nodo_solucion
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(origen)
    resultado.reverse()

    return jsonify({
        'ruta': resultado,
        'mensaje': f'Ruta encontrada: {" → ".join(resultado)}',
        'destino_final': destino
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
