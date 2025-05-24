from google.cloud import vision
import io
import os
import tempfile
import google.generativeai as genai
import re
from dotenv import load_dotenv

load_dotenv()

# 🔑 Tulis kredensial Google Vision dari ENV ke file sementara
def write_credential_file():
    cred_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if cred_json:
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as f:
            f.write(cred_json)
            f.flush()
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name

write_credential_file()

def get_vision_client():
    return vision.ImageAnnotatorClient()

# 🧠 Inisialisasi Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# 🔍 Fungsi OCR
def detect_handwritten_text(image_bytes):
    client = get_vision_client()
    image = vision.Image(content=image_bytes)
    response = client.document_text_detection(image=image)
    if response.error.message:
        print(f"Error dari Google Vision API: {response.error.message}")
        return ""
    return response.full_text_annotation.text

# 🧠 Prompt ke Gemini
def post_process_text(raw_text):
    prompt = f"""
Berikut adalah hasil OCR dari teks tulisan tangan:

"{raw_text}"
Kamu adalah AI yang bertugas merapikan hasil OCR tulisan tangan.
Tolong perbaiki struktur kalimat, ejaan, dan rapikan tata letak. Berikan nomor untuk tiap jawaban yang sesuai dengan ejaan berdasarkan sintaksis bahasa Indonesia yang baik dan benar.
"""
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    response = model.generate_content(prompt)
    return response.text.strip()

# 🧼 Bersihkan format Markdown
def remove_markdown_formatting(text):
    text = re.sub(r"\*\*\*(.*?)\*\*\*", r"\1", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    return text.strip()

# 🌟 UI Utama
def main():
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QFileDialog, QVBoxLayout, QWidget, QRadioButton, QButtonGroup, QMessageBox
    )
    from PyQt6.QtGui import QPixmap
    from PyQt6.QtCore import Qt
    import sys

    class OCRApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("OCR Tulisan Tangan + AI Perapihan (Gemini)")
            self.setGeometry(100, 100, 800, 700)
            self.image_bytes = None
            self.ocr_text = ""
            self.improved_text = ""
            self.cleaned_text = ""

            # Widgets
            self.label = QLabel("Unggah gambar tulisan tangan (png/jpg/jpeg)")
            self.upload_btn = QPushButton("Pilih File Teks Hasil OCR")
            self.upload_btn.clicked.connect(self.open_file)
            # Hapus img_label, tidak perlu lagi
            self.ocr_btn = QPushButton("Proses OCR")
            self.ocr_btn.clicked.connect(self.process_ocr)
            self.ocr_btn.setEnabled(False)
            self.ocr_result = QTextEdit()
            self.ocr_result.setReadOnly(True)
            self.save_ocr_btn = QPushButton("Simpan Hasil OCR")
            self.save_ocr_btn.clicked.connect(self.save_ocr)
            self.save_ocr_btn.setEnabled(False)
            self.gemini_btn = QPushButton("Perbaiki Teks dengan AI (Gemini)")
            self.gemini_btn.clicked.connect(self.process_gemini)
            self.gemini_btn.setEnabled(False)
            self.format_label = QLabel("Pilih Format Teks:")
            self.radio_plain = QRadioButton("Teks Polos")
            self.radio_markdown = QRadioButton("Markdown")
            self.radio_plain.setChecked(True)
            self.radio_group = QButtonGroup()
            self.radio_group.addButton(self.radio_plain)
            self.radio_group.addButton(self.radio_markdown)
            self.radio_plain.toggled.connect(self.update_final_text)
            self.radio_markdown.toggled.connect(self.update_final_text)
            self.final_label = QLabel("Teks Setelah Diperbaiki:")
            self.final_result = QTextEdit()
            self.final_result.setReadOnly(True)
            self.save_final_btn = QPushButton("Simpan Teks Rapi")
            self.save_final_btn.clicked.connect(self.save_final)
            self.save_final_btn.setEnabled(False)

            # Layout
            layout = QVBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.upload_btn)
            # img_label dihapus
            layout.addWidget(self.ocr_btn)
            layout.addWidget(QLabel("Hasil OCR Mentah:"))
            layout.addWidget(self.ocr_result)
            layout.addWidget(self.save_ocr_btn)
            layout.addWidget(self.gemini_btn)
            layout.addWidget(self.format_label)
            layout.addWidget(self.radio_plain)
            layout.addWidget(self.radio_markdown)
            layout.addWidget(self.final_label)
            layout.addWidget(self.final_result)
            layout.addWidget(self.save_final_btn)

            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

        def open_file(self):
            file_path, _ = QFileDialog.getOpenFileName(self, "Pilih File Teks Hasil OCR", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                with open(file_path, "rb") as f:
                    self.image_bytes = f.read()
                self.ocr_btn.setEnabled(True)

        def process_ocr(self):
            if not self.image_bytes:
                return
            self.ocr_result.setPlainText("Memproses OCR...")
            QApplication.processEvents()
            # Asumsikan file sudah hasil OCR, langsung tampilkan
            text = self.image_bytes.decode(errors="ignore")
            if text:
                self.ocr_text = text
                self.ocr_result.setPlainText(text)
                self.save_ocr_btn.setEnabled(True)
                self.gemini_btn.setEnabled(True)
            else:
                self.ocr_result.setPlainText("File kosong atau tidak valid.")
                self.save_ocr_btn.setEnabled(False)
                self.gemini_btn.setEnabled(False)

        def save_ocr(self):
            if not self.ocr_text:
                return
            file_path, _ = QFileDialog.getSaveFileName(self, "Simpan Hasil OCR", "hasil_ocr.txt", "Text Files (*.txt)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.ocr_text)

        def process_gemini(self):
            if not self.ocr_text:
                return
            self.final_result.setPlainText("Memproses dengan Gemini...")
            QApplication.processEvents()
            improved = post_process_text(self.ocr_text)
            cleaned = remove_markdown_formatting(improved)
            self.improved_text = improved
            self.cleaned_text = cleaned
            self.update_final_text()
            self.save_final_btn.setEnabled(True)

        def update_final_text(self):
            if self.radio_plain.isChecked():
                self.final_result.setPlainText(self.cleaned_text)
            else:
                self.final_result.setPlainText(self.improved_text)

        def save_final(self):
            text = self.cleaned_text if self.radio_plain.isChecked() else self.improved_text
            file_path, _ = QFileDialog.getSaveFileName(self, "Simpan Teks Rapi", "hasil_rapi.txt", "Text Files (*.txt)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)

    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    write_credential_file()
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    main()
