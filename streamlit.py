import streamlit as st
import fitz
import pytesseract
from PIL import Image
import speech_recognition as sr
import pyttsx3

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_file_path = r'C:\Users\shilp\OneDrive\Desktop\project\EnglishPart1.pdf'
img_path = r'CC:\Users\shilp\OneDrive\Desktop\project\english.png'

def perform_ocr(image):
    text = pytesseract.image_to_string(image)
    return text

text_speech = pyttsx3.init()

st.header('Athena Learning Helper')

img = Image.open(img_path)
st.image(img, use_column_width=True)

pdf_document = fitz.open(pdf_file_path)
num_pages = pdf_document.page_count

text_speech = pyttsx3.init()
text_speech.say("Welcome to Athena learning helper app. Let's learn Class 12 English Today. you can euther say the page number to be read or Say 0 to read all the pages.also say 'exit' to exit from Athena.")
text_speech.runAndWait()

while True:
    text_speech.say("Please say a page number")
    text_speech.runAndWait()
    r = sr.Recognizer()
    mic = sr.Microphone()
    text = None

    with mic as source:
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print('You Said : ', text)
            text_speech.say('You Said : ' + text)
            text_speech.runAndWait()

            if text.lower() == "exit":
                break 

        except sr.UnknownValueError:
            print("Didn't hear anything, please repeat")
            text_speech.say("Didn't hear anything, please repeat")
            text_speech.runAndWait()

    page_num = None

    if text:
        if text.isdigit():
            page_num = int(text) - 1
        else:
            print("Please say a valid page number")
            text_speech.say("Please say a valid page number")
            text_speech.runAndWait()
            continue

    if page_num is not None:
        if 0 <= page_num < num_pages:
            page = pdf_document[page_num]
            image = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)
            page_text = perform_ocr(image_pil)

            print(f"Page {page_num + 1}:\n{page_text}\n{'=' * 40}\n")
            text_speech.say(page_text)
            text_speech.runAndWait()

        elif page_num == -1:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                image = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)
                page_text = perform_ocr(image_pil)

                print(f"Page {page_num + 1}:\n{page_text}\n{'=' * 40}\n")
                text_speech.say(page_text)
                text_speech.runAndWait()

        else:
            print("Invalid page number.")
            text_speech.say('Invalid page number')
            text_speech.runAndWait()

text_speech.say("Thank you for using Learning Helper.")
text_speech.runAndWait()
