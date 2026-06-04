# Proyecto Final - Sistemas Distribuidos

## Descripción

Proyecto de despliegue de una arquitectura distribuida utilizando OpenTofu, Incus, OVN, Docker, PostgreSQL, FastAPI, Prometheus y Grafana.

La infraestructura se encuentra automatizada mediante OpenTofu y Ansible, permitiendo la creación y configuración de los servicios necesarios para la aplicación.

---

## Arquitectura

La solución está compuesta por los siguientes nodos:

| Nodo 		| IP 	     |
|---------------|------------|
| node-control 	| 10.10.0.5  |
| app-api 	| 10.10.0.10 |
| app-core 	| 10.10.0.11 |
| db-postgres 	| 10.10.0.12 |
| monitoring 	| 10.10.0.20 |
| ceph-node 	| 10.10.0.30 |

Todos los nodos se encuentran conectados mediante la red OVN:

```text
ovn-lab (10.10.0.0/24)
```

## Microservicios mínimos

- app-api: puerta de entrada y exposición REST.
- app-core: reglas de negocio, validaciones y flujo principal.
- db-postgres: persistencia de usuarios, recursos y reservas.
- monitoring: métricas de aplicación y de sistema.
- ceph-node: almacenamiento controlado de respaldos.

---

## Tecnologías utilizadas

- OpenTofu
- Incus
- OVN
- Ubuntu 24.04
- Docker
- FastAPI
- PostgreSQL
- Prometheus
- Grafana
- Node Exporter
- Ansible
- Git

---

## Estructura del proyecto

```text
proyecto-final/
├── ansible
│   ├── docker.yml
│   ├── inventory.ini
│   ├── postgres.yml
│   └── update.yml
├── app-api
│   ├── app
│   │   └── main.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── requirements.txt
├── app-core
│   ├── app
│   │   └── main.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── requirements.txt
├── ceph-node
│   └── backups
│       └── appdb.sql
├── evidencias
│   ├── app-api.txt
│   ├── app-core.txt
│   ├── ceph-node.txt
│   ├── db-postgres.txt
│   ├── incus-list.txt
│   ├── monitoring.txt
│   ├── node-control.txt
│   ├── ovn-lab.txt
│   └── tofu-state.txt
├── monitoring
│   ├── docker-compose.yml
│   ├── grafana-dashboard-1780419875242.json
│   └── prometheus.yml
├── opentofu
│   ├── main.tf
│   ├── terraform.tfstate
│   ├── terraform.tfstate.1780242905.backup
│   └── terraform.tfstate.backup
└── README.md

```

---

## Despliegue de infraestructura

```bash
cd opentofu

tofu init
tofu apply
```

---

## Configuración mediante Ansible

### Actualización de paquetes

```bash
ansible-playbook -i inventory.ini update.yml
```

### Instalación de Docker

```bash
ansible-playbook -i inventory.ini docker.yml
```

### Configuración de PostgreSQL

```bash
ansible-playbook -i inventory.ini postgres.yml
```

---

## API FastAPI

La API expone los siguientes endpoints:

### Login

```http
POST /login
```

### Obtener reservas

```http
GET /reservas
```

### Crear reserva

```http
POST /reservas
```

Ejemplo:

```json
{
  "nombre": "Juan",
  "fecha": "2026-06-02"
}
```

### Eliminar reserva

```http
DELETE /reservas/{id}
```

### Crear recurso

```http
POST /recursos
```

### Obtener recursos

```http
GET /recursos
```

### Eliminar recurso

```http
DELETE /recursos/{id}
```

---

---
### Flujo

```text
Usuario
   |
   v
app-api (10.10.0.10)
   |
HTTP GET /validar
   |
   v
app-core (10.10.0.11)
   |
Respuesta JSON
   |
   v
app-api
   |
   v
Usuario

```

## Monitoreo

### Prometheus

```text
http://10.10.0.20:9090
```

### Grafana

```text
http://10.10.0.20:3000
```

El dashboard exportado se encuentra en:

```text
monitoring/grafana-dashboard-1780419875242.json
```

---

---

## Ceph node

```text
ceph-node

Responsabilidad:
Almacenamiento controlado del sistema.

Funciones:
- Recepción de respaldos de PostgreSQL.
- Conservación de snapshots y archivos de recuperación.
- Separación lógica entre persistencia y almacenamiento.

Flujo:

db-postgres
   |
 pg_dump
   |
   v
ceph-node (/backups)

```

## Evidencias

La carpeta `evidencias` contiene información de validación y pruebas realizadas sobre la infraestructura desplegada.

---

## Autores

Nicolás Orozco,
Oscar García,
Cristhian Alzate

Ingeniería de Sistemas y Computación
Universidad Tecnológica de Pereira
