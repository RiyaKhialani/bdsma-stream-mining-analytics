# Big Data Stream Mining & Social Media Analytics Platform for Digital Marketplaces

[![Institution](https://img.shields.io/badge/Institution-VESIT%20Comp%20Engg-0f172a.svg?style=for-the-badge&logo=google-classroom&logoColor=white)](https://vesit.ves.ac.in)
[![Course](https://img.shields.io/badge/Course-BDSMA%20(Sem%207)-black.svg?style=for-the-badge)](https://vesit.ves.ac.in)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

An enterprise-grade **Big Data Analytics (BDA)** and **Social Media Analytics (SMA)** intelligence surveillance platform designed to combat coordinated review fraud, promotional velocity bursts, and bot rings across digital commerce platforms using **100% authentic, real e-commerce data**.

---

## 👥 Student & Guide Details

* **Institution:** Department of Computer Engineering, Vivekanand Education Society's Institute of Technology (VESIT), University of Mumbai
* **Academic Year:** 2026–2027
* **Under the Guidance of:** Dr. (Mrs.) Nupur Giri & Dr. (Mrs.) Sujata Khedkar

| Student Name | Roll No. |
| :--- | :--- |
| **Riya Khialani** | **34** |
| **Prachi Lund** | **39** |
| **Ankita Kukreja** | **36** |
| **Shivam Makhija** | **41** |

---

## 🏛️ System Architecture

```
                               ┌──────────────────────────────────────────────────────────┐
                               │       High-Velocity E-Commerce Data Streams              │
                               │     (Amazon Catalog, Customer Reviews, Live URLs)        │
                               └────────────────────────────┬─────────────────────────────┘
                                                            │
                               ┌────────────────────────────┴─────────────────────────────┐
                               ▼                                                           ▼
         ┌───────────────────────────────────────────┐           ┌───────────────────────────────────────────┐
         │     Big Data Analytics (BDA) Engine       │           │   Social Media Analytics (SMA) Engine     │
         ├───────────────────────────────────────────┤           ├───────────────────────────────────────────┤
         │ • Bloom Filter (O(1) Bot Blocking)        │           │ • Bipartite Social Network G = (U, P, E)  │
         │ • Count-Min Sketch (Frequency Estimation) │           │ • Co-Review Graph Projection              │
         │ • Reservoir Sampling (Vitter Algorithm R) │           │ • Louvain Modularity Community Detection  │
         │ • MinHash LSH (Near-Duplicate Detection)  │           │ • Centralities (PageRank/FraudRank)       │
         │ • MapReduce Lexicon Indexing              │           │ • Aspect-Based Sentiment Analysis (ABSA)  │
         │ • Real Catalog & Hardware Standards Loader│           │ • Poisson Velocity Burst Modeling         │
         └─────────────────────┬─────────────────────┘           └─────────────────────┬─────────────────────┘
                               │                                                       │
                               └────────────────────────────┬──────────────────────────┘
                                                            ▼
                               ┌──────────────────────────────────────────────────────────┐
                               │        Interactive Surveillance Dashboard (Port 8502)    │
                               │      (Streamlit Web UI + Plotly + Network Visualizer)    │
                               └──────────────────────────────────────────────────────────┘
```

---

## ⚡ Core Mathematical Engines & Algorithms

### 1. Big Data Analytics (BDA) Stream Mining Engine
* **Bloom Filter:** Provides $O(1)$ set membership testing with zero false negatives to block known blacklisted bot reviewers and spam vectors.
* **Count-Min Sketch:** Sub-linear frequency estimation under $(\epsilon, \delta)$ mathematical guarantees ($w = \lceil e/\epsilon \rceil, d = \lceil \ln(1/\delta) \rceil$).
* **Reservoir Sampling (Vitter's Algorithm R):** Fixed-size uniform random sampling maintaining true mathematical unbiasedness over unbounded high-velocity review streams.
* **Locality-Sensitive Hashing (MinHash LSH):** Clusters near-duplicate reviews in sub-quadratic $O(1)$ query time using $k$-shingling and Jaccard similarity estimation.
* **MapReduce Batch Processor:** Distributed-style Map and Reduce phases for parallel complaint indexing and term frequency aggregation.

### 2. Social Media Analytics (SMA) Graph & Sentiment Engine
* **Bipartite Social Graph Modeling:** Formulates relationships as $\mathcal{G} = (\mathcal{U}, \mathcal{P}, \mathcal{E})$, where $\mathcal{U}$ represents reviewer accounts, $\mathcal{P}$ represents products, and edges $\mathcal{E}$ carry rating and temporal attributes.
* **Collusive Review Ring Detection:** Computes co-review projection networks and applies **Louvain Modularity Optimization** to isolate synchronized bot rings with density $\rho > 0.5$.
* **Network Centrality & FraudRank:** Calculates Degree, Betweenness, and modified **PageRank / FraudRank** to detect influential sockpuppet nodes.
* **Aspect-Based Sentiment Analysis (ABSA):** Evaluates sentiment polarities across 6 hardware dimensions (Build Quality, Battery Life, Charging Wattage, Display/UI, Audio, and Value for Money).
* **Poisson Arrival Burst Modeling:** Applies Poisson arrival process modeling to detect anomalous promotional bursts ($Z_t \ge 3.0\sigma$) within 48-hour windows.

---

## 🚀 Quickstart & Setup

### Prerequisites
* Python 3.10+ (Recommended: Python 3.11 or 3.12)
* Git

### Installation

```bash
# Clone the repository
git clone https://github.com/RiyaKhialani/bdsma-stream-mining-analytics.git
cd bdsma-stream-mining-analytics

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Web Platform

```bash
streamlit run bdsma_app.py --server.port 8502
```

Open your browser at **http://localhost:8502** to explore:
1. **Catalog & Stream Explorer:** Real Amazon product catalog and live streaming review samples.
2. **BDA Stream Algorithms:** Interactive Bloom Filter testing, Count-Min frequency monitoring, and MinHash duplicate clustering.
3. **SMA Network Visualizer:** 2D interactive bipartite social networks, reviewer projections, and Louvain fraud ring clusters.
4. **Sentiment & Burst Analytics:** Aspect-based radar charts, polarity breakdown, and Poisson velocity spikes.

---

## 🧪 Running Unit Tests

Execute the comprehensive test suite verifying all 15 algorithmic components:

```bash
python -m unittest tests/test_bdsma_features.py -v
```

All 15 tests pass with 100% coverage across BDA stream algorithms, SMA graph metrics, and ABSA analysis.

---

## 📂 Project Structure

```
bdsma-stream-mining-analytics/
├── bdsma/
│   ├── __init__.py
│   ├── bda_engine.py             # Bloom Filter, Count-Min Sketch, Reservoir, MinHash, MapReduce
│   ├── sma_engine.py             # Bipartite Network, Louvain, Centralities, ABSA, Poisson
│   ├── real_data_loader.py       # Amazon product catalog and review stream loader
│   ├── live_link_parser.py       # Live URL parsing and feature extraction
│   ├── kgirs_engine.py           # Heterogeneous graph construction and multi-hop reasoning
│   ├── nx_compat.py              # NetworkX mathematical helper routines
│   └── data/
│       ├── real_amazon_catalog.json
│       ├── real_amazon_reviews.json
│       └── hardware_spec_standards.json
├── tests/
│   ├── __init__.py
│   └── test_bdsma_features.py    # 15 comprehensive unit tests
├── bdsma_app.py                  # Main Streamlit web application (Port 8502)
├── bdsma_architecture_diagram.png# High-resolution architectural diagram
├── generate_bdsma_diagram.py     # Script to regenerate architecture diagram
├── generate_bdsma_report.py      # Script to generate Word doc report
├── Project_Report_BDSMA.docx     # Complete academic report (Word document)
├── Project_Report_BDSMA.md       # Complete academic report (Markdown format)
├── requirements.txt              # Production Python dependencies
└── README.md                     # Comprehensive project documentation
```

---

## 📜 Academic Integrity & Citation
Developed for academic micro-project evaluation in **Big Data & Social Media Analytics (BDSMA)** at Vivekanand Education Society's Institute of Technology (VESIT), Chembur, Mumbai.
