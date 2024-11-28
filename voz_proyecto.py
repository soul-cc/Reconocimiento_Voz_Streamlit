import streamlit as st
import speech_recognition as sr
from docx import Document
from reportlab.pdfgen import canvas
from io import BytesIO

# Función para reconocer voz
def reconocer_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.info("Por favor, hable ahora...")
        audio = recognizer.listen(source)
        
    try:
        texto = recognizer.recognize_google(audio, language='es-ES')
        return texto
    except sr.UnknownValueError:
        return "No se pudo entender el audio."
    except sr.RequestError:
        return "Error al intentar contactar el servicio de voz de Google."

# Función para generar archivo Word en memoria
def generar_word(texto):
    doc = Document()
    doc.add_paragraph(texto)

    # Crear archivo en memoria
    archivo = BytesIO()
    doc.save(archivo)
    archivo.seek(0)
    return archivo

# Función para generar archivo PDF en memoria
def generar_pdf(texto):
    archivo = BytesIO()
    c = canvas.Canvas(archivo)
    c.drawString(100, 750, texto)
    c.save()
    archivo.seek(0)
    return archivo

# Función para generar archivo de texto en memoria
def generar_txt(texto):
    archivo = BytesIO()
    archivo.write(texto.encode('utf-8'))
    archivo.seek(0)
    return archivo


# Inicializar los valores de session_state si no existen
if 'texto' not in st.session_state:
    st.session_state.texto = ""



# Crear la interfaz de usuario con Streamlit
st.title("Reconocimiento de Voz a Texto")

# Botón para activar el micrófono
if st.button("Hablar"):
    texto = reconocer_voz()
    st.session_state.texto = texto  # Guardar el texto reconocido en session_state
    st.write("Texto reconocido:", texto)

# Mostrar el texto generado y opciones de archivo solo si hay texto
if st.session_state.texto:
    archivo_generado = None

    if st.button("Generar Word"):
        archivo_generado = generar_word(st.session_state.texto)
        st.session_state.word_file = archivo_generado
        st.success("Archivo Word generado. Puedes descargarlo desde aquí:")
        st.download_button("Descargar Word", archivo_generado, file_name="salida.docx")

    if st.button("Generar PDF"):
        archivo_generado = generar_pdf(st.session_state.texto)
        st.session_state.pdf_file = archivo_generado
        st.success("Archivo PDF generado. Puedes descargarlo desde aquí:")
        st.download_button("Descargar PDF", archivo_generado, file_name="salida.pdf")

    if st.button("Generar Bloc de Notas"):
        archivo_generado = generar_txt(st.session_state.texto)
        st.session_state.txt_file = archivo_generado
        st.success("Archivo de texto generado. Puedes descargarlo desde aquí:")
        st.download_button("Descargar TXT", archivo_generado, file_name="salida.txt")