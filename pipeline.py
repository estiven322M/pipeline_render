import psycopg2
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json


def ejecutar_pipeline():

    try:
        
        
        # 🔹 1. Conexión a Render
        conn = psycopg2.connect(
        host="dpg-d70am9ua2pns73b190o0-a.oregon-postgres.render.com",
        database="finances_x2eu",
        user="finances_x2eu_user",
        password="rV3pJlER1legpGxxiusEhogKzm9xjIMX",
        port=5432
        )

        print("✅ Conectado a Render")

        # 🔹 2. Consulta
        query = "SELECT * FROM execution_time;"
        df = pd.read_sql(query, conn)
        conn.close()

        # 🔹 3. Transformación
        df["time"] = df["time"].astype(str)
        df["time"] = pd.to_timedelta(df["time"])
        df["time_ms"] = df["time"].dt.total_seconds() * 1000
        df = df.drop(columns=["time"])

        # 🔹 4. Credenciales desde ENV (CORRECTO)
        creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # 🔹 5. Subir a Google Sheets
        sheet = client.open("datos_algoritmos").sheet1

        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())

        print("✅ Datos enviados a Google Sheets")


    except Exception as e:
        

        print("❌ Error:", e)
