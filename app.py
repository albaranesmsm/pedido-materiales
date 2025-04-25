import streamlit as st
import pandas as pd
import datetime
import smtplib
from email.message import EmailMessage
from openpyxl import Workbook
from io import BytesIO  # <-- corrección
# --- DATOS SMTP (Brevo) ---
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USER = "8b6a63001@smtp-brevo.com"
SMTP_PASSWORD = "JjHRLIE1BD3U2MwC"
# --- DATOS FIJOS ---
COMPRADOR = "612539"
DESTINATARIO = "davidvictores@hotmail.com"
COPIA = "dvictoresg@mahou-sanmiguel.com"
ASUNTO = "TEST ASUNTO"
# --- RELACIÓN ARTÍCULOS Y PROVEEDORES ---
proveedores = {
   "1600043": "13161", "1600050": "13161", "1600051": "13161", "1600052": "13161", "1600053": "13161",
   "1600054": "13161", "1600055": "13161", "1600911": "13161", "1600921": "13161", "1601104": "13161",
   "1601161": "13161", "1601271": "13161", "1601306": "13161", "0400153": "10381", "0400176": "10381",
   "0400177": "10381", "0400232": "10381", "0400543": "10381", "0400548": "10381", "0400699": "10381",
   "1601001": "10381"
}
# --- RELACIÓN ARTÍCULOS Y OB ---
ob_values = {
   "1600043": "14001536", "1600050": "14001536", "1600051": "14001536", "1600052": "14001536",
   "1600053": "14001536", "1600054": "14001536", "1600055": "14001536", "1600911": "14001536",
   "1600921": "14001536", "1601104": "14001536", "1601161": "14001536", "1601271": "14001536",
   "1601306": "14001536", "0400153": "31005151", "0400176": "31005151", "0400177": "31005151",
   "0400232": "31005151", "0400543": "31005151", "0400548": "31005151", "0400699": "31005151",
   "1601001": "31005151"
}
# --- LISTA DE ARTÍCULOS ---
articulos = [
   {"Nº artículo": "1600043", "Descripción": "TUB DESAG PVC//PVC"},
   {"Nº artículo": "1600050", "Descripción": "PYTHON A Inund 1 P"},
   {"Nº artículo": "1600051", "Descripción": "PYTHON A2 Inund 2 P"},
   {"Nº artículo": "1600052", "Descripción": "PYTHON L Contac 1P"},
   {"Nº artículo": "1600053", "Descripción": "PYTHON L2 Contac 2P"},
   {"Nº artículo": "1600054", "Descripción": "PYTHON L3 Contac 3P"},
   {"Nº artículo": "1600055", "Descripción": "TUB AGUA REF"},
   {"Nº artículo": "1600911", "Descripción": "PYTHON COL"},
   {"Nº artículo": "1600921", "Descripción": "LUPULUS 6,35 1P eventos"},
   {"Nº artículo": "1601104", "Descripción": "TUB ARM Riego arm"},
   {"Nº artículo": "1601161", "Descripción": "TUB GAS LDP"},
   {"Nº artículo": "1601271", "Descripción": "KIT ANTI-COND"},
   {"Nº artículo": "1601306", "Descripción": "FLEXLAYER 1P Vermut"},
   {"Nº artículo": "0400153", "Descripción": "DINFEX Antialgas"},
   {"Nº artículo": "0400176", "Descripción": "COMPACT 200 Limp inst."},
   {"Nº artículo": "0400177", "Descripción": "TOPFOAM Limp máq"},
   {"Nº artículo": "0400232", "Descripción": "PLUS ESPEC Limp inst."},
   {"Nº artículo": "0400543", "Descripción": "ALUTRAT Limp inst."},
   {"Nº artículo": "0400548", "Descripción": "ULTR"},
   {"Nº artículo": "0400699", "Descripción": "MULTIUSOS Higiene"},
   {"Nº artículo": "1601001", "Descripción": "PROTECTOR CO2"}
]
# --- INTERFAZ ---
st.title("Generador de pedidos")
st.markdown("Selecciona los artículos y cantidades para generar el pedido.")
pedido = []
for articulo in articulos:
   cantidad = st.number_input(f"{articulo['Descripción']} ({articulo['Nº artículo']})", min_value=0, step=1)
   if cantidad > 0:
       pedido.append({
           "Nº artículo": articulo["Nº artículo"],
           "Descripción": articulo["Descripción"],
           "Cantidad": cantidad,
           "Proveedor": proveedores.get(articulo["Nº artículo"], ""),
           "OB": ob_values.get(articulo["Nº artículo"], "")
       })
email_origen = st.text_input("Tu nombre o correo (solo se mostrará como remitente)")
if st.button("Generar y enviar pedido"):
   if not email_origen:
       st.warning("Por favor, introduce tu nombre o email.")
   else:
       fecha = datetime.datetime.now().strftime("%Y-%m-%d")
       df = pd.DataFrame(pedido)
       df["Comprador"] = COMPRADOR
       df["Fecha"] = fecha
       # Excel a memoria (corregido con BytesIO)
       wb = Workbook()
       ws = wb.active
       ws.title = "Pedido"
       ws.append(df.columns.tolist())
       for row in df.itertuples(index=False):
           ws.append(list(row))
       excel_buffer = BytesIO()
       wb.save(excel_buffer)
       excel_bytes = excel_buffer.getvalue()
       # Email
       msg = EmailMessage()
       msg["Subject"] = ASUNTO
       msg["From"] = email_origen
       msg["To"] = DESTINATARIO
       msg["Cc"] = COPIA
       msg.set_content(f"Hola,\n\nSe adjunta el pedido generado el {fecha}.\n\nUn saludo.")
       msg.add_attachment(
           excel_bytes,
           maintype="application",
           subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
           filename="pedido.xlsx"
       )
       try:
           with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
               smtp.starttls()
               smtp.login(SMTP_USER, SMTP_PASSWORD)
               smtp.send_message(msg)
           st.success("Pedido enviado con éxito.")
       except Exception as e:
           st.error(f"Error al enviar el correo: {e}")
