# Dashboard de Gastos Personales

App web para registrar y visualizar ingresos y gastos personales. Construida con Python Flask y SQLite.

## Funciones

- Registrar ingresos y gastos con categoría, descripción, monto y fecha
- Gráfica de gastos por categoría (dona)
- Gráfica de flujo diario del mes (barras)
- Resumen de ingresos, gastos y balance del mes
- Historial de últimas transacciones
- Filtro por mes
- Eliminar transacciones

## Instalación

### 1. Clona o descarga el proyecto

```bash
git clone https://github.com/Hugorangel123/Dashboard-Gastos.git
cd dashboard-gastos
```

### 2. Crea un entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecuta la app

```bash
python app.py
```

### 5. Abre en el navegador

```
http://localhost:5000
```

La base de datos `gastos.db` se crea automáticamente en la primera ejecución.

## Estructura del proyecto

```
dashboard-gastos/
├── app.py              # Servidor Flask y rutas
├── gastos.db           # Base de datos SQLite (se genera sola)
├── requirements.txt    # Dependencias
├── templates/
│   └── index.html      # Interfaz completa (HTML + CSS + JS)
└── README.md
```

## Tecnologías

- Python 3.x
- Flask 3.x
- SQLite3 (incluido en Python)
- Chart.js (CDN)
- HTML / CSS / JavaScript vanilla

## Posibles mejoras

- Exportar reporte a PDF o Excel
- Agregar metas de ahorro por categoría
- Login con múltiples usuarios
- Notificaciones cuando se supera el presupuesto
