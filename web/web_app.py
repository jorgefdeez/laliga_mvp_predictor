import os
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, send_from_directory


WEB_DIR = Path(__file__).resolve().parent
TOP10_PATH = WEB_DIR / "top10_predictions.csv"
app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")


@app.get("/")
def index():
	return send_from_directory(WEB_DIR, "index.html")


@app.get("/api/top10")
def top10():
	try:
		predictions = pd.read_csv(TOP10_PATH).to_dict(orient="records")
	except FileNotFoundError:
		return jsonify({"error": "Predicciones no disponibles"}), 404
	except (pd.errors.ParserError, OSError):
		return jsonify({"error": "No se pudieron leer las predicciones"}), 500
	return jsonify(predictions)


if __name__ == "__main__":
	app.run(
		host="127.0.0.1",
		port=int(os.environ.get("PORT", "5000")),
		debug=False,
	)

