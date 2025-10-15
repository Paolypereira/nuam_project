🏦 Proyecto NUAM – Integración Bursátil Chile, Colombia y Perú

Este proyecto implementa una API REST y un panel administrativo para la integración bursátil de los países que conforman NUAM (Chile, Colombia y Perú).
Permite gestionar países, empresas, normativas y valores bursátiles, además de cargar automáticamente información desde archivos Excel.

---

🚀 Instalación y Ejecución

1️⃣ Clonar el repositorio

bash

git clone https://github.com/Paolypereira/nuam_project.git

cd nuam_project

2️⃣ Crear entorno virtual

bash
python -m venv .venv

3️⃣ Activar el entorno virtual

.\.venv\Scripts\activate

En macOS / Linux:

bash

Copiar código

source .venv/bin/activate

4️⃣ Instalar dependencias

bash

Copiar código

pip install -r requirements.txt

5️⃣ Aplicar migraciones

bash


Copiar código

python manage.py migrate

6️⃣ Cargar países base (Chile, Colombia, Perú)

bash

Copiar código

python manage.py cargar_paises

7️⃣ Cargar datos desde Excel NUAM

El repositorio incluye el archivo Informe_Bursátil_Regional_2025-08.xlsx

También se entrega una plantilla_carga_nuam.xlsx para futuras cargas.


bash

Copiar código

python manage.py seed_empresas --file "Informe_Bursátil_Regional_2025-08.xlsx"

8️⃣ Crear superusuario (para el panel /admin/)

bash

Copiar código

python manage.py createsuperuser

Usuario preconfigurado para revisión docente:

Usuario: profe

Contraseña: profe1234

9️⃣ Ejecutar el servidor

bash

Copiar código

python manage.py runserver


🌐 Navegación del Proyecto

Funcionalidad	URL	Descripción

🏠 Inicio API	http://127.0.0.1:8000/	                                      Mensaje de bienvenida y rutas principales

🔧 Panel Administrativo	http://127.0.0.1:8000/admin/	                      Administración de países, empresas, normativas y cargas masivas

🌍 API REST	http://127.0.0.1:8000/api/	                                    Endpoints JSON para integraciones externas

📘 Documentación Swagger	http://127.0.0.1:8000/api/docs/	                  Documentación interactiva de la API

🧾 Página pública de empresas	http://127.0.0.1:8000/api/demo/empresas/	    Vista amigable del catálogo de empresas


🧩 Estructura del proyecto

php

Copiar código

nuam_project/
│
├── mercados/                  # App principal (modelos, vistas, admin, serializers)
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── admin.py
│   └── utils_import.py        # Script de carga automática de Excel
│
├── templates/                 # Plantillas HTML (vista demo)
├── static/                    # Estilos y assets
├── db.sqlite3                 # Base de datos local con datos de ejemplo
├── manage.py
├── requirements.txt
├── README.md
└── plantilla_carga_nuam.xlsx  # Plantilla editable para cargas futuras


🧾 Carga masiva desde Excel

Ingresar al panel administrativo

→ Mercados > Archivo carga masivas > Añadir.

Subir un archivo Excel (con estructura similar a plantilla_carga_nuam.xlsx).

Guardar y marcar como procesado.


El sistema leerá automáticamente la hoja correcta (Nemo-Cap. Bur|Ticker-Market Cap)

y actualizará las empresas en base a su ticker y país.


🧠 Tecnologías utilizadas

Python 3.11

Django 5.2

Django REST Framework (DRF)

django-filter

pandas

openpyxl

SQLite3


🧑‍🏫 Credenciales para revisión docente

Rol	Usuario	Contraseña

Profesor / Revisor	profe	profe1234


💬 Notas finales

El proyecto se ejecuta localmente con DEBUG=True por lo que no requiere configuración adicional.


El archivo db.sqlite3 incluye datos cargados de ejemplo.

Se puede regenerar desde cero ejecutando los comandos de carga masiva.

El panel administrativo y la API REST están completamente funcionales.
