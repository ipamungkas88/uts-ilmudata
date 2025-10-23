# Dashboard Visualisasi Data Computer Prices

# Ujian Tengah Semester - Ilmu Data

## 📊 Deskripsi Proyek

Dashboard visualisasi data untuk menganalisis **Harga Komputer dan Spesifikasinya**. Proyek ini mencakup preprocessing data, analisis statistik deskriptif, dan visualisasi interaktif berbasis web menggunakan Flask dengan 100,000+ records data komputer.

## 🎯 Tujuan Proyek

1. ✅ Melakukan preprocessing data computer prices (missing values, duplikat, outliers)
2. ✅ Menghitung statistik deskriptif untuk setiap atribut komputer
3. ✅ Membuat visualisasi data yang informatif tentang harga dan performa
4. ✅ Membangun dashboard web dua halaman dengan Flask
5. ✅ Deploy ke PythonAnywhere.com

## 📁 Struktur Proyek

```
ilmu data/
│
├── flask/
│   ├── app.py                     # Aplikasi Flask utama
│   ├── requirements.txt           # Dependencies Python
│   ├── README.md                  # Dokumentasi proyek
│   │
│   └── templates/                 # Template HTML
│       ├── statistics.html        # Halaman 1: Statistik Deskriptif
│       └── charts.html            # Halaman 2: Visualisasi Charts
│
├── uts.ipynb                      # Jupyter Notebook analisis data
└── computer_prices_all.csv        # Dataset (100,000+ records)
```

## 🚀 Cara Menjalankan Proyek

### 1. Persiapan Environment

```bash
# Buat virtual environment (opsional tapi direkomendasikan)
python -m venv .venv

# Aktivasi virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat

# Install dependencies
pip install flask plotly pandas numpy seaborn matplotlib
```

### 2. Setup Dataset

```bash
# Pastikan file computer_prices_all.csv ada di direktori utama
# File berisi 100,000+ records data komputer
```

### 3. Jalankan Dashboard

```bash
# Masuk ke direktori flask
cd "c:/Users/pamii/Documents/ilmu data/flask"

# Jalankan aplikasi Flask
python app.py
```

Akses dashboard di browser: `http://127.0.0.1:5001`

## 📊 Fitur Dashboard

### 1. Halaman Statistics (`/`)

- Ringkasan statistik dataset computer prices
- Informasi jumlah data: 100,000+ records dengan 27 kolom
- Statistik deskriptif untuk kolom numerik (price, ram, storage, dll)
- Statistik kategorikal untuk brand, OS, processor type
- Data dari cell 7 di uts.ipynb

### 2. Halaman Charts (`/charts`)

- **Scatter Plot**: Harga vs Performance Score
- **Bar Chart**: Top 10 Brand dengan Harga Rata-rata Tertinggi
- **Box Plot**: Sebaran Harga berdasarkan Operating System
- **Histogram**: Distribusi Harga Komputer
- **Correlation Heatmap**: Korelasi antar variabel numerik
- **Pie Chart**: Distribusi Brand Komputer
- **Line Chart**: Trend Harga berdasarkan RAM Size
- **Violin Plot**: Distribusi Harga per Kategori Storage
- **Sunburst Chart**: Hierarki Brand-OS-Price Range
- Semua visualisasi dari cells 10-18 di uts.ipynb

## 🔧 Teknologi yang Digunakan

### Backend

- **Python 3.11.9** - Bahasa pemrograman utama
- **Flask 2.3.3** - Web framework
- **Pandas 2.3.2** - Data manipulation dan analisis
- **NumPy 2.3.2** - Numerical computing
- **Seaborn 0.13.2** - Statistical visualization

### Visualisasi

- **Plotly Graph Objects 5.17.0** - Interactive visualization (UPGRADE dari Plotly Express)
- **Matplotlib 3.10.7** - Static plotting untuk notebook
- **Chart styling**: Professional margins, Arial fonts, 500px height

### Frontend

- **Bootstrap 5.1.3** - CSS framework untuk responsive design
- **HTML5/CSS3** - Markup dan styling dengan modern shadows
- **JavaScript ES6** - Interactivity dan chart rendering

### Dataset

- **computer_prices_all.csv** - 100,000+ records komputer
- **27 kolom** termasuk brand, model, price, specs, performance score

## 📊 Statistik Deskriptif

Untuk setiap atribut numerik komputer:

- **Price**: Mean, Median, Mode, Standard Deviation, Range
- **RAM**: Distribusi memory size (4GB, 8GB, 16GB, 32GB+)
- **Storage**: HDD vs SSD capacity analysis
- **Performance Score**: Composite score berdasarkan specs
- **Screen Size**: Distribusi ukuran layar (13", 15", 17"+)

Untuk setiap atribut kategorikal:

- **Brand**: Frequency analysis (Dell, HP, Lenovo, Asus, etc.)
- **Operating System**: Windows vs MacOS vs Linux distribution
- **Processor Type**: Intel vs AMD market share
- **Graphics**: Integrated vs Dedicated GPU analysis

## 📊 Jenis Visualisasi

1. **Scatter Plot** - Hubungan Harga vs Performance Score
2. **Bar Chart** - Top 10 Brand dengan Harga Rata-rata Tertinggi
3. **Box Plot** - Sebaran Harga berdasarkan Operating System
4. **Histogram** - Distribusi Harga Komputer (0-10M IDR)
5. **Heatmap** - Korelasi antar variabel numerik (price, ram, storage)
6. **Pie Chart** - Market Share Brand Komputer
7. **Line Chart** - Trend Harga berdasarkan RAM Size
8. **Violin Plot** - Distribusi Harga per Kategori Storage
9. **Sunburst Chart** - Hierarki Brand-OS-Price Range
10. **Interactive Plotly Charts** - Semua dengan zoom, hover, dan filter

## 🌐 Deployment ke PythonAnywhere

### Langkah-langkah:

1. **Upload Files**

   - Upload semua file proyek ke PythonAnywhere
   - Gunakan Git atau upload manual folder flask/

2. **Install Dependencies**

   ```bash
   pip install --user flask plotly pandas numpy seaborn matplotlib
   ```

3. **Setup Web App**

   - Buat new web app
   - Pilih Flask framework
   - Python version: 3.11

4. **Configure WSGI File**

   ```python
   import sys
   path = '/home/yourusername/ilmu-data/flask'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```

5. **Upload Dataset**

   - Upload computer_prices_all.csv ke direktori yang tepat
   - Pastikan path dataset sesuai di app_two_pages.py

6. **Reload Web App**

   - Klik tombol "Reload"
   - Akses di: `yourusername.pythonanywhere.com`

## 📝 Materi Presentasi (23 Oktober 2025)

### 1. Dataset (2-3 menit)

- Sumber data: Computer Prices All (Kaggle/dataset publik)
- Struktur dataset: 100,000+ records, 27 kolom
- Deskripsi atribut: Brand, Model, Price, RAM, Storage, OS, Performance Score

### 2. Data Preprocessing (3-4 menit)

- **Missing Values**:
  - Handling missing price dan specs data
  - Metode median untuk numerik, modus untuk kategorikal
- **Performance Score**:
  - Calculated composite score berdasarkan RAM, Storage, Processor
- **Outliers**:
  - Analysis luxury vs budget computers
  - Price range analysis (100K - 50M IDR)

### 3. Analisis Data untuk Dashboard (3-4 menit)

- **Statistik Deskriptif**:
  - Mean price per brand, median RAM size
  - Standard deviation price distribution
- **Visualisasi yang akan ditampilkan**:
  - Price vs Performance correlation
  - Brand market analysis (Dell, HP, Lenovo dominance)
  - OS distribution (Windows 90%+, MacOS, Linux)
  - Storage trends (SSD adoption vs HDD)
- **Insight yang didapat**:
  - Gaming laptops premium segment growth
  - Brand positioning analysis
  - Price-performance sweet spots

## 🎓 Informasi Akademik

- **Mata Kuliah**: Ilmu Data
- **Tugas**: Ujian Tengah Semester
- **Tanggal Presentasi**: 23 Oktober 2025
- **Durasi**: ~10 menit
- **Dataset**: Computer Prices Analysis (100,000+ records)



---

**Dibuat dengan ❤️ untuk Ujian Tengah Semester Ilmu Data 2025**
