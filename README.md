# OCR-Tulisan-tangan
OCR tulisan tangan dengan google vision dan perbaikan hasil OCR dengan Gemini AI


# OhMyHand Desktop

Aplikasi desktop untuk merapikan hasil OCR tulisan tangan menggunakan Google Vision dan AI Gemini, dengan antarmuka modern berbasis PyQt6.

## Fitur
- Membaca file teks hasil OCR tulisan tangan
- Merapikan teks menggunakan AI Gemini (Google Generative AI)
- Pilihan output: teks polos atau markdown
- Simpan hasil ke file
- Tanpa login/password

## Instalasi

1. **Clone repository & masuk ke folder project**
   ```sh
   git clone <repo-anda>
   cd ohmyhand_desktop
   ```

2. **Buat dan isi file .env**
   - Salin `.env.example` menjadi `.env`
   - Isi `GEMINI_API_KEY` dengan API key Gemini Anda
   - Isi `GOOGLE_APPLICATION_CREDENTIALS_JSON` dengan isi file credential Google Vision (format JSON, dijadikan satu baris)

3. **Install dependensi**
   ```sh
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi**
   ```sh
   python app.py
   ```

## Build ke Aplikasi Windows (.exe)

1. Install pyinstaller:
   ```sh
   pip install pyinstaller
   ```
2. Build aplikasi:
   ```sh
   pyinstaller --onefile --windowed app.py
   ```
3. File .exe akan ada di folder `dist/`. Copy file `.env` jika diperlukan.

## Cara Pakai
1. Jalankan aplikasi.
2. Pilih file teks hasil OCR (misal dari Google Vision atau aplikasi OCR lain).
3. Klik "Proses OCR" untuk menampilkan teks mentah.
4. Klik "Perbaiki Teks dengan AI (Gemini)" untuk merapikan teks.
5. Pilih format output (teks polos/markdown).
6. Simpan hasil jika diinginkan.

## Kebutuhan
- Python 3.9+
- API key Gemini (Google Generative AI)
- Credential Google Vision (format JSON, dijadikan satu baris di .env)

## Catatan
- Aplikasi ini tidak membutuhkan login/password.
- File gambar tidak diproses langsung, hanya file teks hasil OCR.
- Untuk keamanan, jangan commit file .env ke repository publik.

---

**Dibuat oleh: [Alfriyan - TIM IT SMK N 1 Pracimantoro]**

Disclaimer:

80% kode digenerate oleh AI, ada kemungkinan bug dan kesalahan parsing
