<div align="center">

# LaLiga MVP Predictor

**Sistema de predicción del MVP de LaLiga EA Sports basado en Machine Learning**
 
Plataforma end-to-end que extrae estadísticas reales de jugadores de LaLiga mediante web scraping,
entrena un modelo de Machine Learning para calcular un índice de rendimiento MVP,
y presenta los resultados a través de una aplicación web interactiva con estética de campo de fútbol.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Servidor-HTTP%20Server-000000?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/Licencia-MIT-green)

</div>

---

## Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Estructura de Directorios](#️-estructura-de-directorios)
- [Funcionalidades Principales](#-funcionalidades-principales)
- [Prerrequisitos y Dependencias](#-prerrequisitos-y-dependencias)
- [Instalación y Configuración](#-instalación-y-configuración)
- [▶Guía de Ejecución](#️-guía-de-ejecución)

---

## Descripción del Proyecto

**LaLiga MVP Predictor** es un proyecto de ciencia de datos que responde a una pregunta:
*¿Quién merece ser el MVP de LaLiga esta temporada según los datos?*

El sistema implementa un **pipeline completo de datos** que cubre desde la extracción de estadísticas
reales de jugadores hasta la visualización final en una interfaz web. Se compone de tres módulos principales:

| Fase | Módulo | Descripción |
|------|--------|-------------|
| **Extracción** | `web_scraping/` | Scraping de estadísticas de jugadores desde fuentes públicas (WhoScored) |
| **Predicción** | `machine_learning/` | Cálculo del índice MVP mediante un scoring ponderado con métricas de eficiencia |
| **Visualización** | `web/` | App web con ranking Top 10 animado sobre un fondo de campo de fútbol |

### Problema que resuelve

Las votaciones del MVP suelen ser subjetivas. Este proyecto propone un enfoque **cuantitativo y reproducible**
que agrega métricas objetivas (goles, asistencias, minutos jugados, tarjetas, eficiencia por minuto)
para generar un ranking transparente y basado en datos de múltiples temporadas (2021/22 – 2026/27).

---

## Estructura de Directorios

```
laliga_mvp_predictor/
│
├── README.md                   # ← Este archivo
├── requirements.txt            # Dependencias de Python
├── setup.sh                    # Script de configuración del entorno
├── run.py                      # Lanzador del pipeline completo
│
├── web_scraping/               # Módulo de extracción y limpieza de datos
│   ├── scraper.ipynb            # Notebook: scraping de estadísticas desde WhoScored
│   ├── data_cleaning.ipynb      # Notebook: limpieza y normalización de datos
│   ├── raw/                     # Datos crudos por temporada
│   │   ├── s2122-laliga-players.csv
│   │   ├── s2223-laliga-players.csv
│   │   ├── s2324-laliga-players.csv
│   │   └── s2425-laliga-players.csv
│   └── processed/              # Datos procesados y listos para ML
│       ├── datos_combinados.csv    # Todas las temporadas unificadas
│       └── datos_limpios.csv       # Datos normalizados y filtrados
│
├── machine_learning/           # Módulo de Machine Learning y ranking
│   ├── machine_learning.ipynb   # Notebook: entrenamiento, scoring y predicción MVP
│   └── jugadores_2627.csv      # Jugadores 2026/27 para filtrar si sigue en la liga el jugador
│
└── web/                        # Aplicación web de visualización
    ├── web_app.py              # Servidor HTTP (Python http.server, puerto 8080)
    ├── index.html              # Frontend: estructura HTML con diseño de campo
    ├── style.css               # Estilos CSS: campo de fútbol, tarjetas, animaciones
    ├── app.js                   # Lógica JS: parseo CSV, render ranking, barras animadas
    └── top10_predictions.csv   # Salida del modelo: Top 10 jugadores con mvp_percentage
```

---

## Funcionalidades Principales

### Módulo de Web Scraping (`web_scraping/`)

| Componente | Funcionalidad |
|-----------|---------------|
| **`scraper.ipynb`** | Extrae estadísticas de jugadores de LaLiga desde fuentes públicas utilizando `requests` y `BeautifulSoup`. Recopila datos como nombre, equipo, edad, posición, partidos, minutos, goles, asistencias, tarjetas y rating. Cubre las temporadas **2021/22 a 2024/25**. |
| **`data_cleaning.ipynb`** | Combina los CSV de todas las temporadas en un único dataset (`datos_combinados.csv`). Normaliza posiciones, limpia campos numéricos, maneja valores nulos, y genera el dataset final `datos_limpios.csv` con las columnas estandarizadas: `player_name`, `team`, `season`, `position`, `minutes_played`, `goals`, `assists`, `yellow_cards`, `red_cards`. |
| **`raw/`** | Almacena los CSV descargados directamente del scraping, uno por temporada. |
| **`processed/`** | Contiene los datasets intermedios y finales del pipeline de limpieza. |

### Módulo de Machine Learning (`machine_learning/`)

| Componente | Funcionalidad |
|-----------|---------------|
| **`machine_learning.ipynb`** | Pipeline completo de análisis y ranking MVP. Carga los datos históricos limpios, calcula promedios por jugador, filtra por mínimo de minutos jugados, y computa tres métricas clave: **`base_score`** (combinación ponderada de goles, asistencias y penalizaciones por tarjetas), **`efficiency`** (rendimiento normalizado por cada 90 minutos), y **`mvp_percentage`** (puntuación relativa al mejor jugador, escala 0-100%). Cruza los datos con las plantillas de la temporada actual (2026/27) y genera el ranking Top 10. |
| **`jugadores_2627.csv`** | Listado de 472 jugadores de la temporada 2026/27 con nombre y equipo, usado para filtrar las predicciones a la temporada actual. |

#### Fórmula del MVP Score

```
base_score = (goals × peso_gol) + (assists × peso_asist) − (yellow × pen_amarilla) − (red × pen_roja)
efficiency = base_score / (minutes_played / 90)
mvp_score  = α × base_score + β × efficiency
mvp_percentage = (mvp_score / max_mvp_score) × 100
```

### Módulo Web (`web/`)

| Componente | Funcionalidad |
|-----------|---------------|
| **`web_app.py`** | Servidor HTTP ligero basado en `http.server` de Python. Sirve archivos estáticos desde el directorio `web/` en el **puerto 8080** y abre automáticamente el navegador al iniciar. |
| **`index.html`** | Estructura de la página con un diseño temático de campo de fútbol (líneas, círculo central, áreas de penalti, corners) y un contenedor para el ranking dinámico. |
| **`style.css`** | ~230 líneas de CSS con variables personalizadas (`--green-dark`, `--accent`, `--gold`), diseño responsive, animaciones hover en las tarjetas de jugador, barras de progreso degradadas, y medallas 🥇🥈🥉 para el podio. |
| **`app.js`** | Carga `top10_predictions.csv` usando la librería **PapaParse**, ordena jugadores por `mvp_percentage`, renderiza el ranking con barras animadas, y aplica sanitización HTML (XSS protection). |
| **`top10_predictions.csv`** | Archivo de salida generado por el notebook de ML. Contiene los 10 mejores jugadores con todas las métricas calculadas. |

### Orquestación (`run.py`)

El lanzador ejecuta el pipeline completo en orden secuencial:

1. **Scraping** → `web_scraping/scraper.ipynb`
2. **Limpieza** → `web_scraping/data_cleaning.ipynb`
3. **Ranking MVP** → `machine_learning/machine_learning.ipynb`
4. **Servidor Web** → `web/web_app.py`

Los notebooks se ejecutan mediante `jupyter nbconvert --execute --inplace`, lo que permite reproducibilidad total del pipeline.

---

## Prerrequisitos y Dependencias

### Requisitos del sistema

| Requisito | Versión mínima | Notas |
|-----------|---------------|-------|
| **Python** | 3.12+ | Recomendado: usar la última versión estable |
| **pip** | 21.0+ | Se actualiza automáticamente con `setup.sh` |
| **python3-venv** | — | Necesario para crear el entorno virtual |
| **Git** | 2.0+ | Para clonar el repositorio |
| **Navegador web** | Moderno | Chrome, Firefox, Edge o Safari (para visualizar la app) |

### Dependencias de Python

Definidas en [`requirements.txt`](requirements.txt):

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `pandas` | 2.2.2 | Manipulación y análisis de DataFrames |
| `numpy` | 2.1.3 | Operaciones numéricas y arrays |
| `scikit-learn` | 1.5.1 | Algoritmos de Machine Learning |
| `requests` | 2.32.3 | Peticiones HTTP para web scraping |
| `beautifulsoup4` | 4.12.3 | Parsing de HTML para extraer datos |
| `Flask` | 3.0.3 | Framework web (disponible como alternativa) |
| `matplotlib` | 3.9.2 | Generación de gráficos y visualizaciones |
| `pytest` | 8.3.2 | Framework de testing automatizado |
| `jupyter` | 1.1.1 | Ejecución de notebooks desde la terminal |

### Dependencias externas (CDN)

| Librería | Uso |
|----------|-----|
| [PapaParse 5.4.1](https://www.papaparse.com/) | Parsing de CSV en el frontend (cargado via CDN) |

---

## Instalación y Configuración

### Clonar el repositorio

```bash
git clone https://github.com/jorgefdeez/laliga_mvp_predictor.git
cd laliga_mvp_predictor
```

### Configuración automática (recomendado)

El script `setup.sh` automatiza todo el proceso: crea el entorno virtual, instala las dependencias y ejecuta los tests.

```bash
chmod +x setup.sh
./setup.sh
```

> [!NOTE]
> El script realiza las siguientes acciones automáticamente:
> 1. Crea un entorno virtual en `.venv/`
> 2. Actualiza `pip` a la última versión
> 3. Instala todas las dependencias de `requirements.txt`
> 4. Ejecuta la suite de tests con `pytest`

### Configuración manual (alternativa)

Si prefieres configurar el entorno paso a paso:

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Verificar la instalación ejecutando los tests
python -m pytest -q
```

### Activar el entorno virtual

Cada vez que abras una nueva terminal, activa el entorno virtual antes de trabajar:

```bash
source .venv/bin/activate
```

> [!TIP]
> Si usas **VS Code**, selecciona el intérprete `.venv/bin/python` para que los notebooks y terminales lo usen automáticamente.

---

## Guía de Ejecución

### Pipeline completo (un solo comando)

Ejecuta todo el flujo de datos de principio a fin:

```bash
source .venv/bin/activate
python run.py
```

Esto ejecuta secuencialmente:

| Paso | Acción | Tiempo aprox. |
|------|--------|---------------|
| 1 | Scraping de datos | ~1-2 min |
| 2 | Limpieza y normalización | ~30 seg |
| 3 | Cálculo del ranking MVP | ~30 seg |
| 4 | Arranque del servidor web | Inmediato |

Una vez completado, se abrirá automáticamente el navegador en:

```
http://localhost:8080
```

Para detener el servidor, pulsa `Ctrl + C` en la terminal.

---

### Ejecución por módulos (individual)

#### Solo Web Scraping

```bash
source .venv/bin/activate
jupyter nbconvert --execute --inplace web_scraping/scraper.ipynb
jupyter nbconvert --execute --inplace web_scraping/data_cleaning.ipynb
```

#### Solo Machine Learning

```bash
source .venv/bin/activate
jupyter nbconvert --execute --inplace machine_learning/machine_learning.ipynb
```

#### Solo la aplicación web

```bash
source .venv/bin/activate
python web/web_app.py
```

> [!IMPORTANT]
> Si el **puerto 8080** está ocupado, el servidor lo detectará automáticamente y mostrará un mensaje indicando que abras el navegador manualmente.

---

### Ejecución interactiva con Jupyter (VS Code)

Para explorar los notebooks paso a paso:

1. Abre el proyecto en **VS Code**
2. Selecciona el intérprete de Python: `.venv/bin/python`
3. Abre cualquier notebook (`.ipynb`) y ejecuta las celdas en orden

Los notebooks disponibles son:

| Notebook | Propósito |
|----------|-----------|
| `web_scraping/scraper.ipynb` | Explorar y ejecutar el scraping de datos |
| `web_scraping/data_cleaning.ipynb` | Inspeccionar la limpieza de datos |
| `machine_learning/machine_learning.ipynb` | Analizar el modelo y ajustar parámetros |

---

### Ejecutar los tests

```bash
source .venv/bin/activate
python -m pytest -q
```

---

### Salidas del proyecto

Una vez ejecutado el pipeline, los archivos de salida generados son:

| Archivo | Ubicación | Contenido |
|---------|-----------|-----------|
| `datos_combinados.csv` | `web_scraping/processed/` | Datos de todas las temporadas unificados |
| `datos_limpios.csv` | `web_scraping/processed/` | Dataset limpio y normalizado |
| `top10_predictions.csv` | `web/` | Top 10 MVP con scores y porcentajes |

---

<div align="center">

Hecho con datos reales de LaLiga

*Temporadas analizadas: 2021/22 · 2022/23 · 2023/24 · 2024/25 → Predicción: 2026/27*

</div>

