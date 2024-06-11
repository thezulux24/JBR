import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'json/key.json'
SPREADSHEET_ID = '1C5a8r5ttZS_eUckkIpiKrhMzScXnNCXe2WuBZY9sfJY'

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
email_user = 'envioreportesjbr@gmail.com'
email_password = 'uogxyadradumrogo'
recep = 'envioreportesjbr@gmail.com'

def send_email(user_email, message, files):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = user_email
    msg['Subject'] = 'Reporte Etica'
    msg.attach(MIMEText(message, 'plain'))

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=file.name)  # use the file's original filename
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    text = msg.as_string()
    server.sendmail(email_user, user_email, text)
    server.quit()
def page1():
    st.markdown("""
    # Línea Ética de la Escuela de Líderes John Boris Rincón
    

    La escuela de Líderes John Boris Rincón pone a disposición de estudiantes activos, egresados, colaboradores y demás grupos de interés la LÍNEA ÉTICA, con el propósito de incentivar el cumplimiento de estándares éticos que nos permiten establecer relaciones de confianza, por lo que a través de este canal puedes reportar la existencia o sospecha de cualquier acto incorrecto como:

    - Uso inadecuado de equipos de computo, mobiliario, materiales de estudio y subsidios destinados para propósitos de la Escuela
    - Consumo de sustancias alucinógenas
    - Relaciones sentimentales entre mayores y menores de edad
    - Situaciones que atenten contra el respeto y la tolerancia en caso de presentarse discrepancia en las preferencias u opiniones políticas, religiosas, de orientación sexual y/o de género y demás dogmas.
    - Violación de normas y políticas del código de Ética propio y de instituciones aliadas.
    - Actos de revelación indebida de información privilegiada o restringida
    - Otros actos que considere contrarios a las normas
    """)

    if st.button("Continuar"):
        st.session_state.page = 2

def page2():
    st.title("Formulario de Reporte")
    user_type = st.selectbox("Selecciona tu tipo de usuario", ["Estudiante activo", "Egresado", "Colaborador", "Familiar"])
    report = st.text_area("Ingresa tu reporte")
    accused = st.text_input("Ingresa a quien deseas denunciar")
    files = st.file_uploader("Sube tus archivos", type=["png", "jpg", "pdf", "xlsx"], accept_multiple_files=True)

    if st.button("Enviar"):
        if user_type and report and accused:
            # Show a message before sending the report
            with st.spinner('Enviando reporte...'):
                attachments = [file for file in files]
                message = f"Tipo de usuario: {user_type}\nReporte: {report}\nAcusado: {accused}"
                send_email(recep, message, attachments)

                values = [
                    [str(datetime.now()), user_type, report, accused],
                ]

                range_ = "JBR!A:D"

                body = {
                    'values': values
                }

                result = service.spreadsheets().values().append(
                    spreadsheetId=SPREADSHEET_ID,
                    range=range_,
                    valueInputOption="USER_ENTERED",
                    body=body
                ).execute()

            st.success("Reporte enviado con exito")
            time.sleep(2)
            # Redirect to the start page
            st.session_state.page = 1
            st.rerun()
        else:
            st.error("Por favor, llena todos los campos antes de enviar.")
def main():
    if "page" not in st.session_state:
        st.session_state.page = 1

    if st.session_state.page == 1:
        page1()
    elif st.session_state.page == 2:
        page2()

if __name__ == "__main__":
    main()