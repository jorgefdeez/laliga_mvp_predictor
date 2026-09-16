# laliga_mvp_predictor

Proyecto base para predecir el MVP de LaLiga con un flujo de extracción, limpieza, entrenamiento y despliegue web.

## Estructura

- `web_scraping/`: extracción y preparación de datos crudos.
- `machine_learning/`: entrenamiento, predicción y modelo entrenado.
- `web/`: aplicación web front-end y backend.
- `tests/`: pruebas automatizadas del pipeline.

## Flujo sugerido

1. Extraer datos desde fuentes públicas o manuales.
2. Limpiar y normalizar los datos en `web_scraping/data_cleaning.py`.
3. Entrenar el modelo con `machine_learning/train.py`.
4. Hacer predicciones con `machine_learning/predict.py`.
5. Exponer la salida a través de `web/web_app.py`.

## Ejecución desde cero

Requisitos:

- Python 3.12 o superior
- `python3-venv`
- VS Code con la extensión Jupyter si quieres ejecutar los notebooks

En Linux:

```bash
cd /home/jorge/Escritorio/laliga_mvp_predictor
chmod +x setup.sh
./setup.sh
source .venv/bin/activate
python run_pipeline.py
```

El comando anterior instala todas las dependencias, ejecuta los tests y arranca el flujo completo en este orden:

1. Extracción en `web_scraping`
2. Limpieza y preparación de datos
3. Ranking MVP
4. Aplicación Flask

Abre http://127.0.0.1:5000.

Para detener Flask, pulsa `Ctrl+C`.

Si el puerto 5000 está ocupado:

```bash
PORT=5001 python web/web_app.py
```

Para ejecutar solamente los tests:

```bash
python -m pytest -q
```

Para ejecutar los notebooks en VS Code, selecciona el intérprete `.venv/bin/python` y ejecuta sus celdas en orden.

## Ranking MVP reproducible

Para ejecutar todo en el orden correcto, empezando por `web_scraping`:

```bash
python run_pipeline.py
```

El lanzador ejecuta extracción, limpieza, ranking y finalmente Flask.

El pipeline de ranking procesa `web_scraping/processed/datos_limpios.csv`, agrega las métricas por jugador, filtra por minutos, calcula `base_score`, `efficiency` y `mvp_percentage`, y genera un Top 10 junto con un gráfico.

```bash
MPLBACKEND=Agg python -m machine_learning.mvp_ranking
```

Salidas:

- `web/mvp_top10_ranking.csv`
- `web/mvp_top10_ranking.png`
