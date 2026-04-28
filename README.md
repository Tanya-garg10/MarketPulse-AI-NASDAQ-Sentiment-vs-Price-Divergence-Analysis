# 📊 MarketPulse AI — NASDAQ Sentiment vs Price Divergence Analysis

A Streamlit-powered dashboard that analyzes NASDAQ 100 stock data (2010–present) to detect potentially mispriced stocks using sentiment vs price divergence.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

- **No Upload Required** — Dataset is pre-loaded from the repo, ready to analyze instantly
- **Interactive Filters** — Select stocks & date range from the sidebar
- **KPI Dashboard** — Quick metrics: stock count, records, date range, avg volatility
- **Closing Price Trend** — Multi-stock line chart comparison
- **Volume Analysis** — Average daily trading volume bar chart
- **Monthly Volatility Heatmap** — Color-coded volatility breakdown by month
- **Mispriced Stock Detection** — Sentiment vs normalized price divergence table & chart
- **Moving Averages** — 20-day & 50-day MA visualization per stock
- **Auto-Generated Insights** — Smart text insights (most mispriced, most volatile, highest volume, etc.)
- **Raw Data Explorer** — Expandable table with CSV download option

---

## 📁 Project Structure

```
├── app.py                          # Main Streamlit application
├── NASDAQ_100_Data_From_2010.csv   # NASDAQ 100 dataset (2010–present)
├── requirements.txt                # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Streamlit** | Web dashboard & UI |
| **Pandas** | Data cleaning & analysis |
| **NumPy** | Numerical computations |

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Tanya-garg10/MarketPulse-AI-NASDAQ-Sentiment-vs-Price-Divergence-Analysis.git
cd MarketPulse-AI-NASDAQ-Sentiment-vs-Price-Divergence-Analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Deploy on Streamlit Cloud

1. Push this repo to GitHub (already done ✅)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo → Main file: `app.py`
5. Click **Deploy**

---

## 📊 Dataset

- **Source:** NASDAQ 100 historical stock data
- **Period:** 2010 – Present
- **Stocks:** 102 companies
- **Records:** ~271,000+ rows
- **Columns:** Date, Open, High, Low, Close, Adj Close, Volume, Name

---

## 🧠 How It Works

1. **Data Loading** — CSV is loaded and cached using `@st.cache_data` for fast reloads
2. **Feature Engineering** — Calculates % change, 20/50-day moving averages, and 20-day rolling volatility
3. **Sentiment Simulation** — Mock sentiment & trend scores are generated (reproducible via seed)
4. **Divergence Detection** — Compares normalized price movement against sentiment to flag mispriced stocks
5. **Auto Insights** — Generates text-based insights from aggregated metrics

---

## 👩‍💻 Author

**Tanya Garg**

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
