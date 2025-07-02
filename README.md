# Plataforma Web para la Administración Segura de Servicios en Servidores Linux

## 📌 Introducción  
Este proyecto es parte de la Experiencia Educativa *Programación Segura*, y tiene como objetivo desarrollar una **plataforma web segura** para la administración remota de servicios en servidores Linux.

## 🎯 Propósito  
Diseñar e implementar una solución web que permita a administradores registrar servidores Linux, gestionar servicios de forma remota y monitorear su estado en tiempo real, cumpliendo con estándares de seguridad y buenas prácticas de desarrollo seguro.

## ✅ Requerimientos

### Rol y Funcionalidades

**Rol requerido:** Administrador  
**Funcionalidades principales:**

- **Registro de Servidores:**  
  - Adición de múltiples servidores Linux.  
  - Registro de servicios por servidor (N servicios por N servidores).  

- **Levantamiento de Servicios:**  
  - Levantar servicios individualmente.  
  - Validación frente a servicios inexistentes o con errores.

- **Administración de Servicios:**  
  - Visualización de servicios activos por servidor.  
  - Acciones disponibles:
    - Reiniciar  
    - Dar de baja  
    - Ver estado  

- **Monitorización:**  
  - Panel de control (dashboard) en tiempo real.  
  - Estado de cada servicio (Activo/Inactivo).  
  - Monitorización periódica automatizada.

### 🔐 Seguridad

- Autenticación segura con contraseña y OTP.  
- Regeneración segura de sesiones.  
- Bloqueo de IP tras múltiples intentos fallidos.  
- Cifrado del archivo `.env`.  
- Modelado de amenazas con DFDs y tablas.

## 🔄 DFDs (Diagramas de Flujo de Datos)

- **DFD Nivel 0**  
- **DFD Nivel 1**  
- **DFD Nivel N**

> Diagramas disponibles en:  
> [Diagrama en diagrams.net](https://app.diagrams.net/#G1rmajD7oRP7UEVOo0qPNuMnyiPfEhhGzL#%7B%22pageId%22%3A%22C5RBs43oDa-KdzZeNtuy%22%7D)

## 🛡️ Tablas de amenazas y mitigaciones

Incluye los siguientes elementos:

- Elementos del sistema  
- Tipos de amenazas asociadas  
- Estrategias de mitigación implementadas  

> Documento disponible en:  
> [Hoja de amenazas y mitigaciones (Google Sheets)](https://docs.google.com/spreadsheets/d/1bqkrJocpoKZAc-KG7rXUTdmRV-b47t5GvxDwki2I7-0/edit?usp=sharing)

## ⚠️ Restricciones

- Exclusivo para servidores con sistema operativo Linux.  
- Manejo seguro de credenciales mediante clave pública.  
- Prohibido almacenar `.env` en texto plano en entornos productivos.

## 🚀 Tecnologías Utilizadas

- **Backend:** Django (Python)  
- **Frontend:** Bootstrap  
- **Conectividad y control:** SSH y Systemctl  
- **Base de datos:** SQLite / MySQL  
- **Cifrado y seguridad:** cryptography (cifrado de archivos y claves)  
- **OTP:** Correo electrónico
