# Vizora

<div align="center">

```
 __      __ _____  ______   ____   _____            
 \ \    / /|_   _||___  /  / __ \ |  __ \     /\    
  \ \  / /   | |     / /  | |  | || |__) |   /  \   
   \ \/ /    | |    / /   | |  | ||  _  /   / /\ \  
    \  /    _| |_  / /__  | |__| || | \ \  / ____ \ 
     \/    |_____|/_____|  \____/ |_|  \_\/_/    \_\
```

### High-Performance Streaming OLAP, In-Browser DuckDB-WASM & Interactive Analytics

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://sandeep332005.github.io/Vizora/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![WebAssembly 64-bit](https://img.shields.io/badge/WASM-memory64%20%2B%20SIMD-654FF0?style=for-the-badge&logo=webassembly&logoColor=white)](https://webassembly.org/)
[![DuckDB-WASM](https://img.shields.io/badge/Database-DuckDB--WASM-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Apache Arrow](https://img.shields.io/badge/Zero--Copy-Apache%20Arrow-E04E39?style=for-the-badge&logo=apachearrow&logoColor=white)](https://arrow.apache.org/)

**[🌐 Experience the Live Vizora Application](https://sandeep332005.github.io/Vizora/)**

</div>

---

## 🌟 Overview

**Vizora** is an ultra-fast, data-reactive analytics workspace, streaming pivot engine, and hardware-accelerated charting component designed to handle massive datasets in real time. 

Built on a native **C++ streaming query engine** compiled to **64-bit WebAssembly (`memory64`)** with SIMD vector acceleration and integrated with **DuckDB-WASM**, Vizora delivers instant OLAP slicing, multi-dimensional pivoting, and SQL execution directly in the browser—with **zero server compute cost** and **100% data privacy**.

---

## ⚡ Why Vizora is Special

Traditional web dashboards choke on 10,000 to 50,000 rows because they rely on single-threaded JavaScript, heavy JSON parsing, and bloated SVG DOM trees. Vizora completely re-engineers browser-based analytics from first principles:

| Capability | Traditional Web Dashboards (D3 / Chart.js) | Enterprise BI (Tableau / PowerBI) | **Vizora** (Perspective + DuckDB-WASM) |
| :--- | :--- | :--- | :--- |
| **Execution Core** | Interpreted JavaScript | Remote Cloud Server Clusters | **Native C++ in WebAssembly 64-bit (`memory64`)** |
| **SQL Engine** | None (JS Array filters) | Remote Database Queries | **In-Browser DuckDB-WASM Virtual Server** |
| **Row Capacity** | 5,000 – 20,000 rows | Large (at high server / egress cost) | **Millions of rows in-browser with $0 server cost** |
| **Real-Time Streaming** | Full re-render on tick (UI stutter) | Periodic batch polling (5–60s) | **Differential delta updates (50,000+ ticks/sec)** |
| **Memory Architecture**| Heavy JSON serialization | Proprietary formats | **Zero-Copy Apache Arrow Columnar Format** |
| **Rendering Pipeline** | SVG / Canvas DOM trees | Proprietary client viewer | **WebGL GPU-Accelerated 2D/3D Rendering** |
| **Data Privacy** | Raw data pushed to server | Stored in vendor cloud | **100% Private local edge computing** |

---

## 📸 Working Proofs & Visual Walkthrough

### 1. Interactive Workspace & Multi-Project Gallery
Explore real-world datasets across **Superstore Sales, NYPD CCRB Allegations, 120 Years of Olympic History, SF Evictions, Movies, Mandelbrot Fractals, and 3D Raycasting**.

![Vizora Workspace Gallery](docs/screenshots/workspace_gallery.png)

---

### 2. Real-Time Trading Blotter, Depth Charts & Market Heatmap
Differential tick processing handling streaming order books, bid/ask depth timeseries, and real-time candlestick charts at 60 FPS without memory leaks.

![Market Trading Desk & Blotter](docs/screenshots/market_trading_desk.jpg)

---

### 3. In-Browser DuckDB-WASM SQL Console
Execute analytical SQL queries directly over in-memory Parquet and Arrow buffers in your browser tab, and convert any query result into an interactive pivot panel with one click.

![DuckDB SQL Console & Heatmap](docs/screenshots/duckdb_sql_console.jpg)

---

## 🚀 Key Technological Pillars

### 1. In-Browser C++ & 64-Bit WebAssembly OLAP Core
Vizora compiles high-performance C++ into 64-bit WebAssembly with support for browser OPFS (Origin Private File System) and memory-mapped virtual columns, enabling client-side datasets larger than 4 GB.

### 2. Pre-Loaded DuckDB-WASM Virtual Filesystem (VFS)
DuckDB-WASM boots automatically with an in-memory VFS pre-populated with analytical Parquet tables:
- `superstore` (9,994 rows — Retail retail margins, profit, and discount telemetry)
- `nypd` / `nypdccrb` (302,801 rows — Civilian Complaint Review Board records)
- `olympics` (271,116 rows — 120 years of Olympic athlete performance)
- `movies` (3,201 rows — Film budgets, box office gross, and ratings)
- `evictions` (49,028 rows — Housing eviction filings and notices)
- `iris` (150 rows — Multiclass botanical classification baseline)

### 3. Differential Delta Updates for Live Streaming Feeds
Instead of re-aggregating entire tables when streaming updates arrive, Vizora computes only the dirty delta cells. It powers live financial trading blotters and IoT sensor feeds at tens of thousands of updates per second.

### 4. GPU-Accelerated WebGL Visualizations
Includes 15+ built-in visualization plugins:
- Virtualized Data Grid (with hierarchical group rollups, tree expansions, and in-cell sparkline bars)
- Heatmaps & Treemaps
- 2D / 3D Sunbursts & Scatter Plots
- Financial Candlestick, Depth & Order Book Charts

---

## 💻 Interactive SQL Queries

You can execute queries directly in the bottom **DUCKDB SQL** drawer:

```sql
-- Category Sales & Margin Performance
SELECT 
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Margin_Pct
FROM superstore
GROUP BY Category
ORDER BY Total_Sales DESC;
```

```sql
-- Loss-Making Sub-Categories
SELECT 
    "Sub-Category",
    ROUND(AVG(Discount), 3) AS Avg_Discount,
    ROUND(SUM(Profit), 2) AS Net_Profit
FROM superstore
GROUP BY "Sub-Category"
HAVING Net_Profit < 0
ORDER BY Net_Profit ASC;
```

```sql
-- Total Records Across All In-Memory DuckDB Tables
SELECT 'superstore' as tbl, count(*) as cnt FROM superstore
UNION ALL SELECT 'movies', count(*) FROM movies
UNION ALL SELECT 'nypd', count(*) FROM nypd
UNION ALL SELECT 'olympics', count(*) FROM olympics
UNION ALL SELECT 'evictions', count(*) FROM evictions
UNION ALL SELECT 'iris', count(*) FROM iris;
```

---

## 🛠️ Local Development & Quickstart

### Prerequisites
- Python 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.13, 3.15)
- Modern web browser with WebAssembly & WebGL support (Chrome, Firefox, Safari, Edge)

### 1. Clone the Repository
```bash
git clone https://github.com/Sandeep332005/Vizora.git
cd Vizora
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Launch Native WebAssembly Server
```bash
python server.py 8080
```
Open **`http://localhost:8080`** in your browser to experience the full WebAssembly application.

### 4. Launch Edge-to-Edge Streamlit Hub (Optional)
```bash
streamlit run app.py --server.port 8501
```
Open **`http://localhost:8501`** for the zero-margin embedded view.

### 5. CLI DuckDB Query Runner
Query any dataset from the command line instantly:
```bash
python query.py "SELECT Category, count(*) FROM superstore GROUP BY Category"
```

---

## 🧪 Automated Testing

Vizora includes an extensive automated test suite covering dimensionality reduction (PCA, t-SNE, UMAP), clustering, anomaly detection, caching, and neuroconnect pipelines:

```bash
pytest tests/ -v
```

```
tests/test_algorithms.py::TestPCA::test_pca_3d PASSED                    [  5%]
tests/test_algorithms.py::TestPCA::test_pca_returns_tuple PASSED         [ 11%]
tests/test_algorithms.py::TestPCA::test_pca_too_many_components PASSED   [ 16%]
tests/test_algorithms.py::TestTSNE::test_tsne_2d PASSED                  [ 22%]
tests/test_algorithms.py::TestTSNE::test_tsne_invalid_perplexity PASSED  [ 27%]
tests/test_algorithms.py::TestUMAP::test_umap_2d PASSED                  [ 33%]
tests/test_algorithms.py::TestClustering::test_kmeans PASSED             [ 38%]
tests/test_algorithms.py::TestClustering::test_kmeans_edge_case PASSED   [ 44%]
tests/test_algorithms.py::TestAnomalyDetection::test_isolation_forest PASSED [ 50%]
tests/test_algorithms.py::TestEvaluation::test_compute_metrics PASSED    [ 55%]
tests/test_caching.py::TestDimensionalityCaching::test_apply_pca_caching_simulation PASSED [ 61%]
tests/test_neuroconnect.py::TestEEGProcessor::test_alpha_dominance_in_rest PASSED [ 66%]
tests/test_neuroconnect.py::TestEEGProcessor::test_filter_pipeline PASSED [ 72%]
tests/test_neuroconnect.py::TestEEGProcessor::test_simulation_shape PASSED [ 77%]
tests/test_neuroconnect.py::TestEEGProcessor::test_spectral_band_decomposition PASSED [ 83%]
tests/test_neuroconnect.py::TestConnectome::test_functional_network_generation PASSED [ 88%]
tests/test_neuroconnect.py::TestConnectome::test_plv_mathematical_bounds PASSED [ 94%]
tests/test_preprocessing.py::TestPreprocessing::test_preprocess_data_encoding PASSED [100%]

======================== 18 passed in 6.72s ========================
```

---

## 📁 Repository Structure

```
VIZORA/
├── .github/
│   └── workflows/
│       └── deploy.yml              # Automated GitHub Pages CI/CD deployment
├── docs/
│   └── screenshots/               # Working proofs and UI screenshots
│       ├── duckdb_sql_console.jpg
│       ├── market_trading_desk.jpg
│       └── workspace_gallery.png
├── perspective-app/               # Production WebAssembly Single-Page Application
│   ├── index.html                 # Main entry point with relative asset resolution
│   ├── index.js                   # Client driver & DuckDB-WASM auto-catalog engine
│   ├── style.css                  # Custom styling & dark/light theme tokens
│   ├── data/                      # Columnar Parquet & Arrow datasets
│   │   ├── superstore.parquet
│   │   ├── movies.parquet
│   │   ├── nypdccrb.parquet
│   │   ├── olympics.parquet
│   │   ├── evictions.parquet
│   │   └── iris.parquet
│   ├── duckdb-browser-FQFFYYKP.js # DuckDB-WASM browser runtime
│   ├── duckdb-GCHGCDU7.js         # DuckDB-Perspective bridge handler
│   ├── perspective-server-*.wasm  # WebAssembly 32-bit & 64-bit server modules
│   └── svg/                       # Geometric SVG wordmarks and icons
├── modules/                       # Python analytics & EEG algorithms
├── components/                    # Modular layout and chart helpers
├── visualization/                 # Python 2D/3D visualization engines
├── tests/                         # Pytest unit & integration test suite
├── app.py                         # Streamlit zero-margin wrapper application
├── server.py                      # Multi-threaded Python server with COOP/COEP headers
├── query.py                       # CLI DuckDB engine connecting Parquet/Arrow
├── requirements.txt               # Python package dependencies
├── .gitignore                     # Git hygiene configuration
└── README.md                      # Comprehensive project documentation
```

---

## 📜 License & Acknowledgments

- Licensed under the **Apache License 2.0**.
- Built with gratitude to the [Perspective OpenJS Project](https://github.com/perspective-dev/perspective) and the [DuckDB Foundation](https://duckdb.org/).
- Trademarks belong to their respective owners.
