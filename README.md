
# 🎬 Real-Time Movie Recommendation System
### **Kafka Streaming • SVD Collaborative Filtering • Automated ML Pipeline**
*Developed as part of **Machine Learning in Production (MLOps)** at Carnegie Mellon University (CMU).*

This project implements a production-style movie recommendation pipeline simulating **1M+ users** and **27k movies**, including Kafka ingestion, ETL, model training, evaluation, and testing.

---

## 📁 Project Structure
```
movie-recommendation-system/
│
├── README.md
├── requirements.txt
│
├── src/
│   ├── data_fetch.py       # Kafka log ingestion
│   ├── data_clean.py       # ETL: build watched/rated datasets
│   ├── Modelling.py        # SVD collaborative filtering (used in pipeline)
│   ├── modelling_final.py  # Alternate model script
│   ├── pipeline.py         # Main pipeline (entry point)
│   ├── hit_rate.py         # Hit-rate & latency evaluation
│
├── tests/
│   ├── test_data_clean.py
│   ├── test_modelling.py
│
├── models/                 # Exported models
├── logs/                   # Kafka logs
└── examples/               # Sample log format
```

---

## 🚀 How to Run

### **1️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

---

## **2️⃣ Run the full pipeline**
Fetch logs *from Kafka* and train the recommendation model:

```bash
python src/pipeline.py --full_pipeline
```

This runs:
- `data_fetch.py` → collects Kafka logs  
- `Modelling.py` → loads cleaned dataset → trains SVD → exports model  

> **Note:** `data_clean.py` is a separate ETL step and must be run manually before training **unless** you already have `watched_rated_df.csv`.

---

## **3️⃣ Run ETL separately (optional)**
If you have raw log files:

```bash
python src/data_clean.py
```

Produces:
- `watched.csv`
- `rated.csv`
- `watched_rated_df.csv` ← used for modelling

---

## **4️⃣ Train model only**
```bash
python src/pipeline.py --train
```

---

## **5️⃣ Fetch logs only (Kafka)**
```bash
python src/pipeline.py --data_collection
```

---

## **6️⃣ Evaluate Hit-Rate & Latency**
```bash
python src/hit_rate.py
```

---

## **7️⃣ Run tests**
```bash
pytest
```

Tests cover:
- Date/integer/request validation  
- Data quality checks  
- RMSE + train/test structure  

---

## 🎓 CMU MLOps Context
This system follows CMU production ML principles:
- Real-time data ingestion (Kafka)  
- Reproducible ETL  
- Collaborative filtering at scale  
- Metric-driven evaluation (RMSE, hit-rate, latency)  
- Modular, testable architecture  

---

## 🌟 Future Enhancements
- FastAPI microservice for real-time recommendations  
- Metadata-based ranking (genres/tags)  
- Incremental training with Kafka streams  
- Docker + CI/CD pipeline  
