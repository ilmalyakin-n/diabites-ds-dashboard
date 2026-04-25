# 🍽️ DiaBites DS Dashboard

Dashboard interaktif berbasis **Streamlit** untuk menganalisis kandungan nutrisi produk makanan Indonesia dan memberikan rekomendasi berdasarkan 7 profil medis (diabetes tipe 1 & 2, hipertensi, diet, atlet, anak, umum).

> Dashboard ini mengintegrasikan 3 analisis utama: OCR photo quality, nutrition dataset distribution, dan product recommendation berbasis RFM segmentation dengan professional data analyst approach.

## Live Dashboard klik di bawah ini:

## [![Streamlit App](https://img.shields.io/badge/Streamlit-Live_Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://diabites.streamlit.app/)

## ✨ Fitur Utama

| Fitur                          | Deskripsi                                                                                                                    |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| **📊 Overview Dashboard**      | Ringkasan total produk, kategori, profil medis, jawaban cepat riset, dan **RFM Analysis** (product segmentation)              |
| **🔬 OCR Insights**            | Analisis mendalam kualitas foto OCR: distribusi kualitas, text extraction length, kategori nutrisi, character vocabulary      |
| **📈 Klasifikasi Analysis**    | Sebaran dataset nutrisi hasil augmentasi: sugar/sodium distribution, nutrient correlation, recommendation by diabetes type    |
| **🎯 Recommendation Simulator**| Simulasi profil pengguna (usia, gender, kondisi, target) untuk menemukan produk paling sesuai kebutuhan nutrisi              |
| **RFM Analysis**               | Product frequency ranking, recommendation rate (quality proxy), segment distribution (High/Moderate/Low quality)              |
| **EDA Visualizations**         | Visualisasi professional dari EDA notebooks: histograms, heatmaps, box plots, bar charts (tanpa overcomplexity)             |

---

## 📁 Struktur Folder

```
diabites-ds-dashboard/
├── app.py                              # Home page - Overview & RFM Analysis
├── pages/
│   ├── 1_OCR_Insights.py               # OCR data quality analysis
│   ├── 2_Klasifikasi_Analysis.py       # Nutrition dataset distribution analysis
│   └── 3_Recommendation_Simulator.py   # Interactive product recommendation testing
├── utils/
│   ├── charts.py                       # Plotly chart functions (bar, histogram, heatmap)
│   ├── common.py                       # Utility functions
│   ├── load_data.py                    # Dataset loaders with caching (@st.cache_data)
│   ├── nutrition.py                    # Scoring logic, medical profiles, nutrition analysis
│   ├── ui.py                           # UI components, CSS injection, sidebar navigation
│   ├── eda_visualizations.py           # Reusable EDA charts from notebooks (NEW)
│   └── rfm_analysis.py                 # RFM analysis functions for product segmentation (NEW)
├── data/
│   ├── nutrition_dataset.csv           # Nutrition data - augmented 7 profiles (11,452 rows)
│   ├── ocr_dataset_quality.csv         # OCR quality labels from image dataset (420 rows)
│   └── ocr_croping_dataset/            # Folder of cropped images for OCR training
├── EDA_code/
│   ├── EDA_data_klasifikasi.ipynb      # EDA analysis of nutrition_dataset.csv
│   ├── EDA_dataocr_croping.ipynb       # Image distribution analysis of OCR dataset
│   ├── EDA_labeldata_ocr.ipynb         # Quality analysis of ocr_dataset_quality.csv
│   └── Gathering, Assessing, Cleaning_dataKlasifikasi.ipynb  # Data pipeline & cleaning
├── .streamlit/
│   └── config.toml                     # Streamlit configuration
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

| Kolom           | Deskripsi                                  |
| --------------- | ------------------------------------------ |
| `product_name`  | Nama produk                                |
| `sugar_g`       | Kandungan gula (gram)                      |
| `carbs_g`       | Kandungan karbohidrat (gram)               |
| `calories`      | Kalori (kkal)                              |
| `sodium_mg`     | Kandungan sodium (mg)                      |
| `fat_g`         | Kandungan lemak (gram)                     |
| `age_group`     | Kelompok usia (child/adult/senior)         |
| `bmi_category`  | Kategori BMI (underweight/normal/overweight/obese) |
| `diabetes_type` | Tipe diabetes (0=normal, 1=type1, 2=type2) |
| `label`         | Rekomendasi (Recommended/Caution/Not Recommended) |

---

## 📊 EDA Analysis Integration

Semua visualisasi di dashboard didasarkan pada hasil analisis dari EDA notebooks untuk memastikan akurasi & insights yang meaningful:

### Nutrition Dataset (EDA_data_klasifikasi.ipynb)
- **Histogram**: Sugar & sodium distribution across products
- **Heatmap**: Correlation matrix of nutritional features (sugar, carbs, calories, sodium, fat)
- **Grouped Bar**: Recommendation distribution by diabetes type (Normal/Type 1/Type 2)
- **Box Plot**: Sugar content by recommendation status

### OCR Quality Dataset (EDA_labeldata_ocr.ipynb)
- **Bar Chart**: Image quality distribution (clear, blur, glare, overlap)
- **Histogram**: Extracted text length distribution (for sequence modeling)
- **Grouped Bar**: Quality levels per nutrition category
- **Bar Chart**: Top 20 most frequent characters (vocabulary analysis)

### Image Dataset Distribution (EDA_dataocr_croping.ipynb)
- **Bar Chart**: Class distribution (image count per nutrient category)
- **Scatter Plot**: Image dimensions analysis (width vs height)
- **Histogram**: Aspect ratio distribution

---

## 🎯 RFM Analysis

**RFM (Recency-Frequency-Monetary) adapted untuk product quality analysis:**

- **Frequency**: How many user profiles/records each product appears in (augmentation multiplier)
- **Monetary Proxy**: Recommendation rate = product quality score (% recommended vs total)
- **Segmentation**: Products classified as High Quality (>70% recommended), Moderate (40-70%), Low (<40%)

**Visualizations:**
- Product frequency ranking (Top 15 products)
- Recommendation rate per product (Quality proxy)
- Category distribution with recommendation rate overlay
- Segment distribution summary (High/Moderate/Low quality counts)

### ocr_dataset_quality.csv

Dataset kualitas foto OCR hasil labeling dari image cropping dataset.

| Kolom       | Deskripsi                                     |
| ----------- | --------------------------------------------- |
| `file_name` | Nama file gambar (e.g., calories_001.png)     |
| `text`      | Teks yang diekstrak dari gambar               |
| `quality`   | Kualitas gambar (clear, blur, overlap, glare) |

### ocr_croping_dataset/ (Folder)

Folders berisi gambar hasil cropping untuk melatih model OCR. Metadata tersimpan di `ocr_dataset_quality.csv`.

---

## 🛠️ Tech Stack

- **Frontend Framework:** [Streamlit](https://streamlit.io) - Interactive web app
- **Visualisasi:** [Plotly](https://plotly.com/python/) - Professional charts with dark theme
- **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Caching:** Streamlit `@st.cache_data` for performance
- **Python:** 3.10+

---

## 📚 Project Workflow

1. **Data Gathering & Cleaning** → `Gathering, Assessing, Cleaning_dataKlasifikasi.ipynb`
2. **EDA & Insights** → `EDA_*.ipynb` files (quality checks, distributions, correlations)
3. **Visualization Design** → Results integrated into `utils/eda_visualizations.py` & `utils/rfm_analysis.py`
4. **Dashboard Implementation** → Streamlit pages (`app.py`, `pages/*.py`) using reusable utility functions
5. **Interactive Testing** → Recommendation Simulator for user profiling

---

## 📜 Lisensi

Dibuat oleh tim Data Science Diabites.

---
