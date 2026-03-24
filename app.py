from flask import Flask
from pipeline import ejecutar_pipeline

app = Flask(__name__)

@app.route("/")
def home():
    return "Servicio activo"

@app.route("/run")
def run():
    ejecutar_pipeline()
    return "✅ Pipeline ejecutado"