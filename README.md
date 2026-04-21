# 🍽️ DiaBites DS Dashboard

Dashboard interaktif berbasis **Streamlit** untuk menganalisis kandungan nutrisi produk makanan Indonesia dan memberikan rekomendasi berdasarkan 7 profil medis (diabetes tipe 1 & 2, hipertensi, diet, atlet, anak, umum).

> Dashboard ini juga menganalisis kualitas foto OCR dari dataset YOLO untuk mengevaluasi seberapa baik informasi nutrisi dapat diekstrak dari foto kemasan produk.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Overview Dashboard** | Ringkasan total produk, kategori, profil medis, dan jawaban cepat pertanyaan riset |
| **Nutrition Analysis** | Filter produk berdasarkan profil & kategori, scatter plot, boxplot, dan analisis risiko diabetes |
| **Recommendation Simulator** | Simulasi profil pengguna untuk menemukan produk paling sesuai kebutuhan nutrisi |
| **Analisis Kualitas Foto OCR** | Visualisasi kualitas gambar dari `yolo_dataset_quality.csv` (distribusi kualitas, masalah foto, heatmap nutrisi vs kualitas) |
| **Insight Otomatis** | Insight berbasis data yang dihasilkan secara otomatis dari dataset |
| **Validasi Dataset** | Pengecekan kolom otomatis — dashboard tetap berjalan meskipun ada kolom yang hilang |

---

## 📁 Struktur Folder

```
diabites-ds-dashboard/
├── app.py                              # Halaman utama (Overview)
├── pages/
│   ├── 2_Nutrition_Analysis.py         # Halaman Nutrition Analysis
│   └── 3_Recommendation_Simulator.py   # Halaman Recommendation Simulator
├── utils/
│   ├── charts.py                       # Fungsi chart Plotly (bar, histogram, heatmap, dll)
│   ├── common.py                       # Fungsi utilitas umum
│   ├── load_data.py                    # Loader dataset dengan caching
│   ├── nutrition.py                    # Logika scoring, profil medis, dan analisis nutrisi
│   └── ui.py                          # Komponen UI, CSS, sidebar, hero, cards
├── data/
│   ├── nutrition_dataset.csv           # Dataset nutrisi produk (11.452 baris)
│   └── yolo_dataset_quality.csv        # Dataset kualitas foto OCR (420 baris)
├── .streamlit/
│   └── config.toml                     # Konfigurasi Streamlit
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Cara Menjalankan Lokal

### Prasyarat

- Python 3.10+
- pip

### Langkah

```bash
# 1. Clone repository
git clone git@github-portofolio:ilmalyakin-n/diabites-ds-dashboard.git
cd diabites-ds-dashboard

# 2. Buat virtual environment (opsional tapi disarankan)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan dashboard
streamlit run app.py
```

Dashboard akan terbuka di `http://localhost:8501`.

---

## ☁️ Deploy ke Streamlit Cloud

1. Push repository ke GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io).
3. Klik **New app** dan hubungkan repository GitHub.
4. Isi konfigurasi:
   - **Repository:** `ilmalyakin-n/diabites-ds-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Klik **Deploy**.

> Pastikan file `requirements.txt` sudah ada di root project.

---

## 📊 Dataset

### nutrition_dataset.csv

Dataset utama berisi informasi nutrisi produk makanan Indonesia.

| Kolom | Deskripsi |
|-------|-----------|
| `product_name` | Nama produk |
| `sugar_g` | Kandungan gula (gram) |
| `carbs_g` | Kandungan karbohidrat (gram) |
| `calories` | Kalori |
| `sodium_mg` | Kandungan sodium (mg) |
| `fat_g` | Kandungan lemak (gram) |
| `age_group` | Kelompok usia |
| `bmi_category` | Kategori BMI |
| `diabetes_type` | Tipe diabetes (0, 1, 2) |
| `label` | Label rekomendasi asli |

### yolo_dataset_quality.csv

Dataset kualitas foto OCR dari model YOLO.

| Kolom | Deskripsi |
|-------|-----------|
| `file_name` | Nama file gambar |
| `text` | Teks yang diekstrak dari gambar |
| `quality` | Kualitas gambar (clear, blur, overlap, glare) |

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io)
- **Visualisasi:** [Plotly](https://plotly.com/python/) (template `plotly_dark`)
- **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Bahasa:** Python 3.10+

---

## 📸 Screenshot

<!-- Tambahkan screenshot dashboard di sini -->
<!-- ![Overview](screenshots/overview.png) -->
<!-- ![Nutrition Analysis](screenshots/nutrition_analysis.png) -->
<!-- ![Recommendation Simulator](screenshots/recommendation_simulator.png) -->

*Screenshot akan ditambahkan setelah deploy.*

---

## 📜 Lisensi

Project ini dibuat untuk keperluan riset dan edukasi.

---

Dibuat dengan ❤️ menggunakan Streamlit.
