# Sistem Monitoring Risiko Keterlambatan

Sistem monitoring dan analitik berbasis AI untuk mengelola risiko keterlambatan pengiriman last-mile menggunakan dataset LaDe.

## Fitur Utama

### 🔮 Prediksi Risiko Real-time
- Model XGBoost untuk prediksi pelanggaran SLA dengan akurasi tinggi
- Monitoring risiko secara real-time
- Intervensi proaktif berdasarkan prediksi

### 🎛️ Simulasi What-If
- Sesuaikan ambang batas risiko dan parameter biaya
- Lihat dampak finansial secara langsung
- Optimalkan strategi intervensi

### 💹 Evaluasi Dampak Ekonomi
- Terjemahkan probabilitas model ke nilai Rupiah
- Minimalkan total biaya penalti dan intervensi
- Analisis cost-benefit untuk keputusan bisnis

### 📊 Dashboard Eksekutif
- KPI strategis dan metrik kinerja
- Wawasan bisnis untuk pengambilan keputusan
- Visualisasi dampak finansial

## Struktur Proyek

```
lade_xgb_decision_web/
├── backend/
│   ├── app.py                 # FastAPI server utama
│   ├── train_model.py         # Training model XGBoost
│   ├── feature_engineering.py # Rekayasa fitur
│   ├── inference.py           # Prediksi real-time
│   ├── decision_policy.py     # Mesin kebijakan keputusan
│   ├── cost_evaluation.py     # Evaluasi biaya
│   ├── what_if.py             # Simulasi what-if
│   └── analytics.py           # Analitik eksekutif
├── frontend/
│   ├── index.html             # Halaman beranda
│   ├── dataset.html           # Penjelajah dataset
│   ├── dashboard.html         # Dashboard operasi
│   ├── simulation.html        # Simulasi what-if
│   ├── executive.html         # Tampilan eksekutif
│   ├── css/
│   │   └── style.css          # Styling aplikasi
│   └── js/
│       ├── dashboard.js       # Logika dashboard
│       ├── simulation.js      # Logika simulasi
│       └── executive.js       # Logika eksekutif
└── data/
    └── lade_sample.csv        # Dataset LaDe (sampel)
```

## Instalasi

1. Clone repository:
```bash
git clone <repository-url>
cd Delay-Risk-Monitoring-System/lade_xgb_decision_web
```

2. Install dependencies Python:
```bash
pip install -r backend/requirements.txt
```

3. Jalankan backend server:
```bash
cd backend
python app.py
```

4. Buka browser dan akses:
```
http://localhost:8000
```

## Penggunaan

### Dashboard Operasi
- Monitoring pengiriman aktif dan prediksi pelanggaran
- Visualisasi distribusi risiko
- Daftar tindakan yang diperlukan

### Simulasi What-If
- Sesuaikan ambang batas risiko (0.0 - 1.0)
- Atur biaya SLA terlewat dan biaya intervensi
- Lihat dampak pada total biaya dan volume intervensi

### Tampilan Eksekutif
- Total eksposur risiko dalam Rupiah
- Efisiensi intervensi dan tingkat kepatuhan
- Wawasan strategis dan rekomendasi

## Teknologi

- **Backend**: FastAPI, Python
- **ML**: XGBoost, scikit-learn, pandas
- **Frontend**: HTML, CSS, JavaScript
- **Visualisasi**: Chart.js
- **Dataset**: LaDe (Last-mile Delivery) dari HuggingFace

## Lisensi

MIT License