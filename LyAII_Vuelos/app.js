const API = 'http://127.0.0.1:5000/api';

const state = {
    ciudades: [],
    currentCity: null,
    phase: 'origin',
    history: [],
};

// DOM
const locationCard = document.getElementById('locationCard');
const currentCityEl = document.getElementById('currentCity');
const selectLabel = document.getElementById('selectLabel');
const citySelect = document.getElementById('citySelect');
const actionBtn = document.getElementById('actionBtn');
const routeCard = document.getElementById('routeCard');
const routePath = document.getElementById('routePath');
const historyCard = document.getElementById('historyCard');
const historyList = document.getElementById('historyList');

// ── Fetch cities ─────────────────────────────
async function init() {
    try {
        const res = await fetch(`${API}/ciudades`);
        const data = await res.json();
        state.ciudades = data.ciudades;
        populateSelect(state.ciudades);
    } catch {
        alert('Error: No se pudo conectar con la API');
    }
}

function populateSelect(cities, exclude) {
    citySelect.innerHTML = '<option value="">— Elige una ciudad —</option>';
    cities
        .filter(c => c !== exclude)
        .forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            citySelect.appendChild(opt);
        });
}

function updateUI() {
    if (state.phase === 'origin') {
        selectLabel.textContent = 'Selecciona tu origen';
        actionBtn.textContent = 'Establecer origen';
        locationCard.style.display = 'none';
        routeCard.style.display = 'none';
        populateSelect(state.ciudades);
    } else {
        selectLabel.textContent = `¿A dónde quieres ir desde ${state.currentCity}?`;
        actionBtn.textContent = 'Buscar ruta';
        locationCard.style.display = '';
        currentCityEl.textContent = state.currentCity;
        populateSelect(state.ciudades, state.currentCity);
    }
    citySelect.value = '';
    actionBtn.disabled = true;
}

function renderRoute(ruta) {
    routeCard.style.display = '';
    routePath.innerHTML = '';
    ruta.forEach(city => {
        const div = document.createElement('div');
        div.className = 'route-step';
        div.innerHTML = `<span class="dot"></span><span>${city}</span>`;
        routePath.appendChild(div);
    });
}

function addHistory(origen, destino, steps) {
    state.history.unshift({ origen, destino, steps });
    if (state.history.length > 8) state.history.pop();
    historyCard.style.display = '';
    historyList.innerHTML = '';
    state.history.forEach(h => {
        const li = document.createElement('li');
        li.textContent = `${h.origen} → ${h.destino}  (${h.steps} escala${h.steps !== 1 ? 's' : ''})`;
        historyList.appendChild(li);
    });
}

// ── Events ───────────────────────────────────
citySelect.addEventListener('change', () => {
    actionBtn.disabled = !citySelect.value;
});

actionBtn.addEventListener('click', async () => {
    const city = citySelect.value;
    if (!city) return;

    if (state.phase === 'origin') {
        state.currentCity = city;
        state.phase = 'destination';
        updateUI();
    } else {
        actionBtn.disabled = true;
        actionBtn.textContent = 'Buscando...';
        try {
            const res = await fetch(`${API}/buscar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ origen: state.currentCity, destino: city }),
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error);
            renderRoute(data.ruta);
            addHistory(state.currentCity, city, data.ruta.length - 1);
            state.currentCity = data.destino_final;
            updateUI();
        } catch (err) {
            alert(err.message);
            actionBtn.disabled = false;
            actionBtn.textContent = 'Buscar ruta';
        }
    }
});

// ── Init ─────────────────────────────────────
init();
updateUI();
