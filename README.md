# NUAM – Mantenedor Bursátil (Django + DRF)

Este proyecto integra datos reales del informe bursátil NUAM (Chile, Colombia, Perú) en una API REST con panel de administración y vista demo.

---

## 🚀 Instalación

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activarlo
# En Windows:
.\.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Cargar países base
python manage.py cargar_paises

# 6. Cargar datos desde Excel NUAM
python manage.py seed_empresas --file "Informe_Bursátil_Regional_2025-08.xlsx"

# 7. Crear superusuario (para /admin/)
python manage.py createsuperuser

# 8. Ejecutar servidor
python manage.py runserver
