import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import smtplib


# CSS personalizado

# Configura tu correo electrónico y contraseña
email_user = 'thezulux@gmail.com'
email_password = 'tuakehjlxgenlsoj'
recep = 'thezulux@gmail.com'

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
    st.title("Objetivo de la línea de ética")
    st.text("'Aun en desarrollo'.")# Aquí puedes agregar el contenido de la primera página
    if st.button("Continuar"):
        st.session_state.page = 2

def page2():
    st.title("Formulario de Reporte")

    st.session_state.user_type = st.selectbox("Selecciona tu tipo de usuario", ["Estudiante activo", "Egresado", "Colaborador", "Familiar"])
    st.session_state.report = st.text_area("Ingresa tu reporte")
    st.session_state.accused = st.text_input("Ingresa a quien deseas denunciar")
    st.session_state.files = st.file_uploader("Sube tus archivos", type=["png", "jpg", "pdf", "xlsx"], accept_multiple_files=True)

    if st.button("Enviar"):
        if st.session_state.user_type and st.session_state.report and st.session_state.accused:
            attachments = [file for file in st.session_state.files]
            message = f"Tipo de usuario: {st.session_state.user_type}\nReporte: {st.session_state.report}\nAcusado: {st.session_state.accused}"
            send_email(recep, message, attachments)
            st.success("Reporte enviado con exito")
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