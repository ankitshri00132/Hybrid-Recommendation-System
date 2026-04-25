<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.56-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-1.8-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" />
  <img src="https://img.shields.io/badge/DVC-3.67-945DD6?style=for-the-badge&logo=dvc&logoColor=white" />
  <img src="https://img.shields.io/badge/Dask-Parallel-FDA061?style=for-the-badge&logo=dask&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS-Deployment-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" />
</p>

<h1 align="center">🎵 Hybrid Music Recommendation System</h1>

<p align="center">
  <b>An end-to-end, production-grade music recommendation engine combining Content-Based Filtering, Collaborative Filtering — built on ~50K songs and ~9.7M user interaction records.</b>
</p>

<p align="center">
  <a href="#-architecture">Architecture</a> •
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-project-structure">Project Structure</a> •
  <a href="#-dvc-pipeline">DVC Pipeline</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

---

## 🏗 Architecture

```
                              ┌───────────────────────┐
                              │     Streamlit UI      │
                              │   (app.py – cached)   │
                              └──────────┬────────────┘
                                         │
                          ┌──────────────┴──────────────┐
                          ▼                              ▼
               ┌──────────────────┐          ┌──────────────────────┐
               │  Content-Based   │          │    Collaborative     │
               │    Filtering     │          │      Filtering       │
               │ (NearestNeighbors│          │  (Cosine Similarity  │
               │  + Cosine Metric)│          │  on Sparse Matrices) │
               └────────┬─────────┘          └─────────┬────────────┘
                        │                              │
                        ▼                              ▼
               ┌──────────────────┐          ┌──────────────────────┐
               │  ColumnTransformer│         │   Dask DataFrame     │
               │  • CountEncoder  │          │   Chunked Processing │
               │  • OneHotEncoder │          │   of 9.7M rows       │
               │  • TF-IDF        │          │         │             │
               │  • StandardScaler│          │         ▼             │
               │  • MinMaxScaler  │          │  Sparse Interaction  │
               └────────┬─────────┘          │  Matrix (CSR)        │
                        │                    └──────────────────────┘
                        ▼
               ┌──────────────────┐
               │  Transformed     │
               │  Sparse Matrix   │
               │  (.npz)          │
               └──────────────────┘
```

The system follows a **two-phase design**:

| Phase | Approach | Status |
|-------|----------|--------|
| **Phase 1** | Content-Based + Collaborative Filtering → Hybrid (weighted sum) | 🔨 In Progress |
| **Phase 2** | Neural Collaborative Filtering (NCF) | 📋 Planned |

---

## ✨ Features

### Currently Implemented
- **Exploratory Data Analysis** — Deep analysis of the Spotify dataset with rich visualizations (distributions, correlations, feature exploration)
- **Content-Based Filtering** — Recommends songs based on audio features, artist, tags, and metadata using a K-Nearest Neighbors model with cosine distance
- **Collaborative Filtering** — Recommends songs based on user listening patterns using cosine similarity on a user-track interaction matrix
- **Streamlit Web App** — Interactive UI with song & artist input, selectable filtering method, configurable number of recommendations (5/10/15/20), and embedded Spotify audio previews
- **Efficient Caching** — `@st.cache_data` and `@st.cache_resource` decorators to eliminate redundant data loading across Streamlit reruns
- **Large-Scale Data Processing** — Dask-based chunked processing of the 9.7M-row `User_Listening_History.csv` (~575 MB) to handle memory constraints
- **Sparse Matrix Representations** — Interaction matrices and transformed feature matrices stored as `scipy.sparse` CSR matrices for memory-efficient computation
- **DVC Pipeline** — Reproducible, versioned 3-stage ML pipeline with full dependency tracking
- **Data Version Control** — Raw datasets (`Music_Info.csv`, `User_Listening_History.csv`) tracked via `.dvc` files, with data git-ignored

### Upcoming
- **Hybrid Recommender** — Weighted combination of content-based and collaborative scores
- **Cold-Start Handling** — Fallback strategy for new users/songs with no interaction history
- **CI/CD Pipeline** — Automated testing and deployment
- **Dockerization** — Containerized application for consistent environments
- **Remote DVC Storage** — S3-backed data versioning for team collaboration
- **AWS Deployment** — Blue-Green deployment strategy for zero-downtime releases
- **Neural Collaborative Filtering (Phase 2)** — Deep learning–based recommendation using learned embeddings

---

## 🛠 Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.10+ |
| **ML / Data Science** | scikit-learn, SciPy, NumPy, Pandas, category_encoders |
| **Large-Scale Processing** | Dask (parallel DataFrame operations for 9.7M rows) |
| **Feature Engineering** | TF-IDF Vectorizer, OneHotEncoder, CountEncoder, StandardScaler, MinMaxScaler |
| **Similarity / Model** | NearestNeighbors (brute-force cosine), Cosine Similarity |
| **Visualization** | Matplotlib, Seaborn (EDA notebooks) |
| **Web App** | Streamlit |
| **Pipeline & Versioning** | DVC (Data Version Control) |
| **Serialization** | Joblib (models & transformers), SciPy npz (sparse matrices), NumPy npy (arrays) |
| **Planned** | Docker, GitHub Actions (CI/CD), AWS (EC2/ECS, S3), Neural Collaborative Filtering |

---

## 📂 Project Structure

```
hybrid-recommender-system/
│
├── app.py                            # Streamlit application (caching, UI, recommendation display)
│
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py              # Raw data cleaning → cleaned_music_data.csv
│   ├── content_based_filtering.py    # ColumnTransformer training, NearestNeighbors model
│   └── collaborative_filtering.py    # Dask-based interaction matrix, cosine similarity CF
│
├── notebook/
│   ├── EDA_Spotify_Dataset.ipynb             # Exploratory Data Analysis
│   ├── Spotify_Content_Based_Filtering.ipynb # CBF prototyping & experiments
│   └── Spotify_Collaborative_Filtering.ipynb # CF prototyping & experiments
│
├── data/
│   ├── raw/
│   │   ├── Music_Info.csv              # ~50K songs (14.9 MB) — DVC-tracked
│   │   ├── Music_Info.csv.dvc
│   │   ├── User_Listening_History.csv  # ~9.7M rows (575 MB) — DVC-tracked
│   │   └── User_Listening_History.csv.dvc
│   └── processed/
│       ├── cleaned_music_data.csv      # Cleaned song metadata (13.7 MB)
│       ├── transformed_data.npz        # Sparse feature matrix for CBF (4.5 MB)
│       ├── collab_filtered_data.csv    # Songs filtered to those in user history (8.3 MB)
│       ├── interaction_matrix.npz      # Sparse user-track interaction matrix (32.3 MB)
│       └── track_ids.npy               # Ordered track ID array for CF (640 KB)
│
├── models/
│   └── nearest_neighbor_cbf.joblib     # Trained NearestNeighbors model (11.1 MB)
│
├── transformer.joblib                  # Trained ColumnTransformer (135 KB)
│
├── dvc.yaml                            # DVC pipeline definition (3 stages)
├── dvc.lock                            # Locked pipeline state with hashes
├── .dvcignore                          # DVC ignore patterns
├── .gitignore                          # Git ignore (data, models, artifacts)
├── requirements.txt                    # Pinned Python dependencies
└── README.md                           # ← You are here
```

---

## 🔄 DVC Pipeline

The ML pipeline is managed by DVC with **3 stages** and full dependency tracking:

![Alt text](assets/pipeline.png)

Reproduce the entire pipeline with:
```bash
dvc repro
```

---

## 🔍 How It Works

### Content-Based Filtering

1. **Data Cleaning** — Deduplication by `spotify_id`, dropping irrelevant columns (`genre`, `spotify_id`), filling missing `tags`, lowercasing text fields
2. **Feature Engineering** — A `ColumnTransformer` applies five parallel transformations:
   - **Frequency Encoding** (`CountEncoder`) on `year`
   - **One-Hot Encoding** on `artist`, `time_signature`, `key`
   - **TF-IDF Vectorization** (`max_features=85`) on `tags`
   - **Standard Scaling** on `duration_ms`, `loudness`, `tempo`
   - **Min-Max Scaling** on `danceability`, `energy`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`
3. **Model Training** — A `NearestNeighbors` model with cosine distance (`algorithm='brute'`) is fitted on the sparse transformed matrix
4. **Recommendation** — Given a (song, artist) pair, the model finds the K+1(which includes the current song) nearest neighbors and returns the top-K similar songs

### Collaborative Filtering

1. **Large-Scale Ingestion** — The 9.7M-row `User_Listening_History.csv` (~575 MB) is loaded using **Dask DataFrames** for memory-efficient, chunk-based parallel processing
2. **Interaction Matrix** — User-track interactions (play counts) are aggregated and stored as a `scipy.sparse.csr_matrix` for memory efficiency
3. **Recommendation** — Given a song, its interaction vector is compared against all other tracks using cosine similarity, and the top-K most similar tracks are returned

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git
- DVC

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ankitshri00132/Hybrid-Recommendation-System.git
cd Hybrid-Recommendation-System

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull data with DVC (currently local storage — S3 remote coming soon)
dvc pull

# 5. Reproduce the pipeline (optional — run if data/models are stale)
dvc repro

# 6. Launch the Streamlit app
streamlit run app.py
```

### Usage

1. Open the Streamlit app in your browser (default: `http://localhost:8501`)
2. Enter a **song name** and **artist name**
3. Select the filtering method: **Content-Based** or **Collaborative**
4. Choose how many recommendations you want (5 / 10 / 15 / 20)
5. Click **Get Recommendation** — enjoy the results with embedded Spotify audio previews 🎧

---

## 📊 Datasets

| Dataset | Description | Size | Rows |
|---------|-------------|------|------|
| `Music_Info.csv` | Song metadata — name, artist, audio features, tags, Spotify preview URLs | 14.9 MB | ~50,000 |
| `User_Listening_History.csv` | User-track play counts | 575 MB | ~9,700,000 |

**Key Features in Music_Info:**
`track_id` · `name` · `artist` · `spotify_preview_url` · `tags` · `genre` · `year` · `duration_ms` · `danceability` · `energy` · `key` · `loudness` · `speechiness` · `acousticness` · `instrumentalness` · `liveness` · `valence` · `tempo` · `time_signature`

**User Listening History Columns:**
`user_id` · `track_id` · `playcount`

---

## 🗺 Roadmap

### Phase 1 — Classical ML (In Progress)

- [x] Exploratory Data Analysis with visualizations
- [x] Data cleaning & preprocessing pipeline
- [x] Content-Based Filtering (NearestNeighbors + cosine distance)
- [x] Collaborative Filtering (cosine similarity on interaction matrix)
- [x] Dask integration for large-scale user history processing
- [x] Streamlit UI with audio previews & caching
- [x] DVC pipeline with 3 reproducible stages
- [x] DVC data tracking (local storage)
- [ ] Hybrid Recommender (weighted sum of CBF + CF scores)
- [ ] Cold-Start problem handling
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Dockerization
- [ ] Remote DVC storage (AWS S3)
- [ ] AWS deployment (Blue-Green strategy)

### Phase 2 — Deep Learning (Planned)

- [ ] Neural Collaborative Filtering (NCF) with learned user/item embeddings
- [ ] Model comparison & A/B testing framework
- [ ] Performance benchmarking (NCF vs. classical approaches)

---

## 📐 Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Dask over Pandas** for user history | The 9.7M-row dataset (~575 MB) exceeds comfortable in-memory processing; Dask enables chunked, parallel computation without loading everything into RAM |
| **Sparse matrices (CSR)** | Both the interaction matrix and transformed feature matrix are highly sparse; CSR format reduces memory from GBs to MBs |
| **NearestNeighbors with brute-force** | With ~50K songs, brute-force cosine search is fast enough and avoids approximation errors from tree-based methods |
| **ColumnTransformer pipeline** | Cleanly applies heterogeneous transformations (encoding, scaling, vectorization) in a single, reproducible step |
| **TF-IDF on tags** (`max_features=85`) | Captures the most informative tag terms while keeping dimensionality manageable |
| **Streamlit caching** | `@st.cache_data` for DataFrames/arrays, `@st.cache_resource` for the ML model — eliminates redundant I/O on every UI rerun |
| **DVC pipeline** | Ensures reproducibility and tracks data/model lineage; will extend to S3 remote for team collaboration |
| **Blue-Green Deployment** (planned) | Zero-downtime deployments on AWS with instant rollback capability |

---

## 🧪 Notebooks

| Notebook | Purpose |
|----------|---------|
| `EDA_Spotify_Dataset.ipynb` | Comprehensive exploratory analysis — distributions, correlations, feature insights |
| `Spotify_Content_Based_Filtering.ipynb` | Prototyping & evaluating the content-based recommendation approach |
| `Spotify_Collaborative_Filtering.ipynb` | Prototyping & evaluating the collaborative filtering approach with Dask |

---
