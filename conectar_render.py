import psycopg2
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
try:
     # 🔹 1. Conexión a Render
    conn = psycopg2.connect(
        host= "dpg-d70am9ua2pns73b190o0-a.oregon-postgres.render.com",
        database="finances_x2eu",
        user="finances_x2eu_user",
        password="rV3pJlER1legpGxxiusEhogKzm9xjIMX",
        port=5432
    )

    print("✅ Conectado a Render")
    # 🔹 2. Consulta (tu tabla de algoritmos)

    query = f"SELECT * FROM execution_time;"
    df=pd.read_sql(query,conn)
    
    # 🔹 Convertir time a string
    df["time"] = df["time"].astype(str)

    # 🔹 Convertir a timedelta
    df["time"] = pd.to_timedelta(df["time"])

    # 🔹 Convertir a milisegundos
    df["time_ms"] = df["time"].dt.total_seconds() * 1000

    # 🔹 Opcional: eliminar columna original
    df = df.drop(columns=["time"])


    conn.close()
    print("\n Datos obtenidos:")
    # 🔹 3. Conectar a Google Sheets
    scope=[
	"https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
     ]
    creds=ServiceAccountCredentials.from_json_keyfile_name(
       "proyecto-algoritmos-credenciales.json", scope
    )
    client =gspread.authorize(creds)
    sheet=client.open("datos_algoritmos").sheet1
    
    # 🔹 4. Subir datos
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("Datos enviados a Google Sheets")

except Exception as e:

    print("❌ Error:", e)
