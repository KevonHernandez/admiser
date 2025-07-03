function actualizarEstados() {
    fetch(URL_VERIFICAR_ESTADOS)
        .then(response => response.json())
        .then(data => {
            const estados = data.estados;
            for (const id in estados) {
                const span = document.getElementById(`estado-servicio-${id}`);
                if (span) {
                    span.textContent = estados[id];
                    span.className = estados[id]; 
                }
            }
        })
        .catch(error => {
            console.error('Error al obtener estados:', error);
        });
}
function ejecutarAccion(servicioId, accion) {
    const url = `/servicio/${accion}/${servicioId}/`;

    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error('Error en la petición');
        return res.json();
      })
      .then(data => {
        const led = document.getElementById(`estado_led_${servicioId}`);
        if (data.estado) {
          if (led) {
            led.classList.remove('activo', 'inactivo', 'sin conexion');
            led.classList.add(data.estado);
          }
        }
        alert(data.resultado || `Estado: ${data.estado}`);
      })
      .catch(err => alert("Error: " + err.message));
  }


// Cargar estados al inicio y cada 10 segundos
document.addEventListener('DOMContentLoaded', actualizarEstados);
setInterval(actualizarEstados, 10000);
