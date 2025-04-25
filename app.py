import streamlit as st
import pandas as pd
import datetime
import smtplib
from email.message import EmailMessage
from io import BytesIO
from openpyxl import Workbook
# --- CONFIGURACIÓN SMTP ---
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USER = "albaranesmsm@outlook.es"
SMTP_PASSWORD = "JjHRLIE1BD3U2MwC"
DESTINATARIO = "davidvictores@hotmail.com"
COPIA = "dvictoresg@mahou-sanmiguel.com"
ASUNTO = "TEST ASUNTO"
# --- FUNCIÓN PARA CREAR EL EXCEL EN MEMORIA ---
def crear_excel(df):
   output = BytesIO()
   wb = Workbook()
   ws = wb.active
   ws.title = "Pedido"
   ws.append(df.columns.tolist())
   for row in df.itertuples(index=False):
       ws.append(list(row))
   wb.save(output)
   output.seek(0)
   return output.getvalue()
# --- FUNCIÓN PARA ENVIAR EL CORREO ---
def enviar_correo(excel_bytes):
   msg = EmailMessage()
   msg["Subject"] = ASUNTO
   msg["From"] = SMTP_USER
   msg["To"] = DESTINATARIO
   msg["Cc"] = COPIA
   msg.set_content("Adjunto el pedido de materiales.")
   msg.add_attachment(
       excel_bytes,
       maintype="application",
       subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
       filename="pedido_materiales.xlsx"
   )
   with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
       server.starttls()
       server.login(SMTP_USER, SMTP_PASSWORD)
       server.send_message(msg)
# --- STREAMLIT APP ---
st.title("Pedido de Materiales")
# Simulación de entrada de datos (puedes reemplazar esto con tu lógica real)
if st.button("Generar Pedido"):
   pedido = [
       {
           "Fecha solicitud": datetime.date.today(),
           "OB": "123456",
           "Comprador": "612539",
           "LM aux": "00004014",
           "Cód Prov": "13161",
           "Proveedor": "",
           "Suc/planta": 8040,
           "Dir entr": "8042",
           "Nº artículo": "1600043",
           "Descripción": "TUB DESAG PVC//PVC",
           "Autorizar cant": 100
       }
   ]
   df = pd.DataFrame(pedido)
   excel_bytes = crear_excel(df)
   enviar_correo(excel_bytes)
   st.success("Pedido generado y enviado por correo.")
   st.download_button("Descargar Excel", data=excel_bytes, file_name="pedido_materiales.xlsx")
