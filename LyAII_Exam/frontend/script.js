// Data del grafo de ciudades
const conexiones = {
    'CDMX': ['JILOTEPEC', 'QRO', 'HIDALGO', 'MORELOS', 'SLP', 'TAMAULIPAS', 'MONTERREY', 'ZACATECAS'],
    'HIDALGO': ['CDMX', 'MORELOS'],
    'MORELOS': ['CDMX', 'HIDALGO'],
    'JILOTEPEC': ['QRO', 'CDMX'],
    'MONTERREY': ['CDMX'],
    'TAMAULIPAS': ['CDMX', 'GUADALAJARA'],
    'QRO': ['JILOTEPEC', 'SLP', 'CDMX', 'ZACATECAS'],
    'GUADALAJARA': ['ZACATECAS'],
    'SLP': ['ZACATECAS', 'QRO'],
    'ZACATECAS': ['CDMX', 'QRO'],
};

// Implementación del Árbol (Nodo)
class Nodo {
    constructor(datos, padre = null) {
        this.datos = datos;
        this.padre = padre;
        this.hijos = [];
    }

    setHijos(hijos) {
        this.hijos = hijos;
        for (let h of this.hijos) {
            h.padre = this;
        }
    }

    getDatos() { return this.datos; }
    getPadre() { return this.padre; }

    igual(nodo) {
        return this.getDatos() === nodo.getDatos();
    }

    enLista(lista) {
        return lista.some(n => this.igual(n));
    }
}

// Algoritmo BFS para rutas
function buscar_solucion_BFS(estado_inicial, solucion) {
    let solucionado = false;
    let nodos_visitados = [];
    let nodos_frontera = [];

    let nodoInicial = new Nodo(estado_inicial);
    nodos_frontera.push(nodoInicial);

    while (!solucionado && nodos_frontera.length !== 0) {
        let nodo = nodos_frontera.shift();
        nodos_visitados.push(nodo);

        if (nodo.getDatos() === solucion) {
            solucionado = true;
            return nodo;
        } else {
            let dato_nodo = nodo.getDatos();
            let lista_hijos = [];

            let hijos_posibles = conexiones[dato_nodo] || [];

            for (let un_hijo of hijos_posibles) {
                let hijo = new Nodo(un_hijo);
                lista_hijos.push(hijo);

                if (!hijo.enLista(nodos_visitados) && !hijo.enLista(nodos_frontera)) {
                    nodos_frontera.push(hijo);
                }
            }
            nodo.setHijos(lista_hijos);
        }
    }
    return null;
}

// Interfaz Gráfica
document.addEventListener('DOMContentLoaded', () => {
    const solveBtn = document.getElementById('solve-btn');
    const btnText = solveBtn.querySelector('span');
    const loader = document.getElementById('loader');

    const initialStateInput = document.getElementById('initial-state');
    const goalStateInput = document.getElementById('goal-state');

    const resultsContainer = document.getElementById('results-container');
    const pathVisualizer = document.getElementById('path-visualizer');
    const stepsCount = document.getElementById('steps-count');
    const errorMsg = document.getElementById('error-msg');

    const showError = (msg) => {
        errorMsg.textContent = msg;
        errorMsg.style.display = 'block';
        resultsContainer.style.display = 'none';
        setTimeout(() => { errorMsg.style.display = 'none'; }, 4000);
    };

    const renderPath = (path) => {
        pathVisualizer.innerHTML = '';
        stepsCount.textContent = path.length - 1;

        path.forEach((state, index) => {
            const stepCard = document.createElement('div');
            stepCard.className = 'step-card';

            const stepNum = document.createElement('div');
            stepNum.className = 'step-number';
            stepNum.textContent = index === 0 ? 'Inicio' : `Paso ${index}`;

            const stepState = document.createElement('div');
            stepState.className = 'step-state';

            const el = document.createElement('div');
            el.className = 'step-element';
            el.textContent = state;

            stepState.appendChild(el);

            stepCard.appendChild(stepNum);
            stepCard.appendChild(stepState);

            pathVisualizer.appendChild(stepCard);
        });

        resultsContainer.style.display = 'block';
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    };

    solveBtn.addEventListener('click', () => {
        const estado_inicial = initialStateInput.value;
        const solucion = goalStateInput.value;

        if (!estado_inicial || !solucion) {
            showError("Asegúrate de seleccionar origen y destino válidos.");
            return;
        }

        btnText.style.display = 'none';
        loader.style.display = 'block';
        solveBtn.disabled = true;

        setTimeout(() => {
            const nodoFinal = buscar_solucion_BFS(estado_inicial, solucion);

            if (nodoFinal) {
                let resultado = [];
                let nodo = nodoFinal;
                while (nodo.getPadre() !== null) {
                    resultado.push(nodo.getDatos());
                    nodo = nodo.getPadre();
                }
                resultado.push(estado_inicial);
                resultado.reverse();

                renderPath(resultado);
            } else {
                showError("No se encontró una ruta posible entre estas ciudades.");
            }

            btnText.style.display = 'inline';
            loader.style.display = 'none';
            solveBtn.disabled = false;
        }, 300);
    });
});
