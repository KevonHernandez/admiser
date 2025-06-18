# Plataforma Web para la Administración Segura de Servicios en Servidores Linux

## 📌 Descripción General

Este proyecto es parte de la **Experiencia Educativa Programación Segura**, y tiene como objetivo desarrollar una plataforma web segura para la **administración remota de servicios en servidores Linux**.

La plataforma permite a un administrador:
- Registrar múltiples servidores Linux
- Levantar y controlar servicios de forma remota
- Monitorear el estado de los servicios en tiempo real

---

## 👤 Rol y Funcionalidades

### Rol: Admin

#### 🔐 Registro de Servidores
- Es posible agregar una N cantidad de servidores con N servicios.
  
#### ⚙️ Levantar Servicios
- Por cada servidor registrado, es posible levantar servicios individualmente
- Validación ante servicios inexistentes o errores de ejecución

#### 🔄 Administración de Servicios
- Visualización de todos los servicios activos por servidor
- Acciones posibles:
  - **Reiniciar**
  - **Dar de baja**
  - **Ver estado**

#### 📊 Monitorización
- Panel de control (Dashboard) actualizado automáticamente
- Estado de cada servicio: **Activo / Inactivo**
- Monitorización periódica.

---

## 🔐 Seguridad

- Autenticación mediante contraseña segura y OTP
- Sesiones protegidas y regeneración segura
- Bloqueo de IP tras múltiples intentos fallidos
- Cifrado del archivo `.env`.
- Modelado de amenazas documentado en DFDs y tablas

---

## 📊 Modelado de Amenazas

- Modelado de amenazas Nivel 0, Nivel 1 y Nivel N
- Tablas de elementos, amenazas y mitigaciones
- Documento disponible en:  https://docs.google.com/spreadsheets/d/1bqkrJocpoKZAc-KG7rXUTdmRV-b47t5GvxDwki2I7-0/edit?usp=sharing
---

Diagrama de flujo de datos: Nivel 0 y 1
Documento disponible en: https://drive.google.com/file/d/1vxexBkIEXkxEwxQoNMK66w4UPTkCKjCz/view?usp=drive_link

## 📦 Entregables

- Documento PDF del proyecto:
  - Introducción
  - Propósito
  - Requerimientos
  - DFDs
  - Tablas de amenazas y mitigaciones

---


## ⚠️ Restricciones

- Uso exclusivo de servidores Linux
- Manejo seguro de credenciales (vía clave pública)
- No debe usarse `.env` en texto plano en producción

---

## 🚀 Tecnologías Usadas

- Django (Python)
- Bootstrap (Frontend)
- SSH / Systemctl (Back-end de control)
- SQLite / MySQL (según entorno)
- `cryptography` (cifrado de configuración)
- Email (para OTP)

---


## 📜 Licencia

Este proyecto es de uso académico bajo fines educativos.  
Todos los derechos reservados © 2025.
