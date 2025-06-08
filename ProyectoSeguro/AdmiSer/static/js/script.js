const serviciosDisponibles = ["Apache", "MySQL", "Nginx", "PostgreSQL"];

const servidores = [
  {
    nombre: "Servidor A",
    estado: true,
    servicios: [
      { nombre: "Apache", estado: true },
      { nombre: "MySQL", estado: false }
    ]
  },
  {
    nombre: "Servidor B",
    estado: false,
    servicios: [
      { nombre: "Nginx", estado: false },
      { nombre: "PostgreSQL", estado: false }
    ]
  }
];

function renderDashboard() {
  const dashboard = document.getElementById("dashboard");
  dashboard.innerHTML = "";

  servidores.forEach((srv, i) => {
    const card = document.createElement("div");
    card.className = "col-md-6 mb-4";

    const opciones = serviciosDisponibles.map(svc =>
      `<option value="${svc}">${svc}</option>`
    ).join("");

    const serviciosHTML = srv.servicios.map(
      (svc, j) => `
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <span class="status-dot ${svc.estado ? "status-active" : "status-inactive"} me-2"></span>
            ${svc.nombre}
          </div>
          <div>
            <button class="btn btn-sm btn-warning me-1" onclick="reiniciar(${i}, ${j})">Reiniciar</button>
            <button class="btn btn-sm btn-danger" onclick="darDeBaja(${i}, ${j})">Dar de baja</button>
          </div>
        </li>`
    ).join("");

    card.innerHTML = `
      <div class="card card-server shadow-sm">
        <div class="card-body">
          <h5 class="card-title d-flex justify-content-between align-items-center">
            ${srv.nombre}
            <span class="badge ${srv.estado ? "bg-success" : "bg-danger"}">${srv.estado ? "Activo" : "Inactivo"}</span>
          </h5>

          <ul class="list-group mt-3">
            ${serviciosHTML}
          </ul>

          <form class="d-flex mt-3" onsubmit="return agregarServicio(event, ${i})">
            <select class="form-select me-2" id="servicioSelect${i}" required>
              <option value="" disabled selected>Selecciona un servicio</option>
              ${opciones}
            </select>
            <button class="btn btn-primary" type="submit">Agregar servicio</button>
          </form>
        </div>
      </div>
    `;

    dashboard.appendChild(card);
  });
}

function reiniciar(i, j) {
  alert(`Reiniciando servicio ${servidores[i].servicios[j].nombre}`);
}

function darDeBaja(i, j) {
  alert(`Dando de baja servicio ${servidores[i].servicios[j].nombre}`);
  servidores[i].servicios[j].estado = false;
  renderDashboard();
}

function agregarServicio(event, i) {
  event.preventDefault();
  const select = document.getElementById(`servicioSelect${i}`);
  const nombre = select.value;
  if (nombre) {
    const yaExiste = servidores[i].servicios.some(s => s.nombre === nombre);
    if (!yaExiste) {
      servidores[i].servicios.push({ nombre, estado: true });
    } else {
      alert("El servicio ya está registrado.");
    }
    renderDashboard();
  }
}
