# 🌟 Phishing URL & Network Security Detection System

# Project Live Link
https://networksecurity-gvj8.onrender.com



### *An End-to-End Enterprise Machine Learning Pipeline for Real-Time Phishing Website Classification, automated with Data Drift Detection, MLflow Tracking, and FastAPI Web Service.*

[![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0+-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3.2-F7931E.svg?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.9.2-0194E2.svg?style=flat-square&logo=mlflow&logoColor=white)](https://mlflow.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.6.1-47A248.svg?style=flat-square&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![DagsHub](https://img.shields.io/badge/DagsHub-MLOps-10A37F?style=flat-square)](https://dagshub.com/)

---

## 📋 Executive Summary
This production-grade machine learning project addresses a critical cybersecurity challenge: **Phishing Website Detection**. 

Traditional phishing defense strategies rely heavily on blacklisting malicious domain names. However, modern phishing websites are highly ephemeral, remaining active for only a few hours to bypass lists. This system overcomes that limitation by employing a **supervised machine learning framework** to extract and evaluate multidimensional URL, domain, and traffic characteristics in real-time.

Built upon an industry-standard modular architecture, this project implements a complete **MLOps pipeline** that automates everything from data ingestion via **cloud MongoDB atlas**, data quality checks with **statistical dataset drift detection (K-S Test)**, robust preprocessing using **KNN Imputation**, automated multiple-model benchmarking/hyperparameter optimization, live experiment logging using **MLflow & DagsHub**, and real-time inference via a highly performant **FastAPI microservice**.

---

## 🛡️ The Cybersecurity Problem & Feature Engineering

### The Phishing Attack Vector
Phishing is a deceptive social engineering practice where malicious actors mimic legitimate corporations to compromise user credentials, steal financial information, or distribute malware.

### Feature Analysis
This system ingests **30 distinct network, structural, and behavioral features** extracted from active web resources to classify URLs as **Phishing (0)** or **Legitimate (1)**.

These features fall into four major categories:
1. **Address Bar Based Features:** Verifying anomalies in the URL structure (e.g., `having_IP_Address`, `URL_Length`, `Shortining_Service`, `having_At_Symbol`, `double_slash_redirecting`, `Prefix_Suffix`, `having_Sub_Domain`, `SSLfinal_State`, `Domain_registeration_length`).
2. **Abnormal Features:** Discrepancies between hostnames and page content (e.g., `Favicon`, `port`, `HTTPS_token`, `Request_URL`, `URL_of_Anchor`, `Links_in_tags`, `SFH`, `Submitting_to_email`, `Abnormal_URL`).
3. **HTML & JavaScript Features:** Dynamic behavior of the web page (e.g., `Redirect`, `on_mouseover` status alterations, `RightClick` disabling, `popUpWidnow` injection, `Iframe` embedding).
4. **Domain & Traffic Metrics:** Global popularity and server identity metrics (e.g., `age_of_domain`, `DNSRecord`, `web_traffic` Alexa rank, `Page_Rank`, `Google_Index`, `Links_pointing_to_page`, `Statistical_report`).

---

## ⚙️ Core Architectural Capabilities & MLOps

This project is built from the ground up to follow **enterprise-grade software engineering** and **MLOps best practices**:

### 1. Data Ingestion & Cloud Decoupling
* **MongoDB Integration:** Ingestion starts by loading cloud credentials and pulling streaming network data directly from a cloud-hosted MongoDB Atlas cluster, decoupled from local files.
* **Stratified Splitting:** Data is dynamically partitioned into train and test sets to maintain class ratio integrity.
* **Database Seeding Tool:** Includes a utility (`push_data.py`) to convert, structure, and seed raw CSV logs directly into the production database.

### 2. Statistical Data Drift Detection (K-S Test)
* Incorporates a robust **Data Validation** phase before preprocessing to check for schema compliance (e.g., verifying column counts against `schema.yaml`).
* Implements dynamic **Covariate Dataset Drift Detection** using the non-parametric **Kolmogorov-Smirnov (K-S) two-sample test** (`scipy.stats.ks_2samp`). This identifies whether incoming real-world evaluation datasets differ significantly from the model's training distribution.
* Saves structured YAML reports detailing p-values and drift status for every single feature.

### 3. Pipeline Data Transformation
* **Imputation Engine:** Utilizes a **K-Nearest Neighbors Imputer (`KNNImputer`)** pipeline to automatically and intelligently reconstruct missing or incomplete network metrics.
* **Label Standardizer:** Automatically maps binary classification outputs from legacy formats (like `-1`/`1`) into normalized, industry-standard targets (`0` for Phishing, `1` for Legitimate).
* **Object Serialization:** Serializes the trained preprocessing pipeline (`preprocessor.pkl`) to guarantee exactly reproducible transformations between training and live batch inference.

### 4. Multiple Ensemble Benchmarking & Tuning
Trains, benchmarks, and hyperparameter-tunes multiple advanced classification ensembles:
* **Random Forest Classifier**
* **Gradient Boosting Classifier (GBM)**
* **AdaBoost Classifier**
* **Decision Tree Classifier**
* **Logistic Regression**

### 5. Remote Experiment Tracking & MLOps
* Fully integrated with **MLflow** tracked remotely on **DagsHub**.
* Automatically logs hyperparameter search spaces, trained models, and evaluated scoring parameters (F1 Score, Precision, Recall).
* Ensures absolute reproducibility and compliance with model audit logs.

### 6. Production Microservice (FastAPI)
* Implements an asynchronous web server using **FastAPI** and **Uvicorn**.
* **`/train` Route:** Empowers users to trigger the entire training and optimization pipeline dynamically.
* **`/predict` Route:** Facilitates batch inference via CSV uploads, executes transformations, generates predictions, stores outputs, and serves a modern, dynamic, clean HTML tabular summary in the browser.

---

## 🏗️ Technical Pipeline & Data Flow

```text
  [ Raw Data (phisingData.csv) ]  ──►  [ Database Seeder (push_data.py) ]
                                                   │
                                                   ▼
                                         [ Cloud MongoDB Atlas ]
                                                   │
                                                   ▼
┌─────────────────────────────────── TRAINING PIPELINE (app.py /train) ───────────────────────────────────┐
│                                                                                                         │
│  [ Data Ingestion ] ──► [ Data Validation ] ──► [ Data Transformation ] ──► [ Model Training & Tuning ] │
│         │                      │                         │                           │                  │
│   (Train/Test Split)     (Schema Check)             (KNN Imputer)              (Grid Search CV)         │
│                                │                         │                           │                  │
│                                ▼                         ▼                           ▼                  │
│                         (K-S Drift Report)      (preprocessor.pkl)           (model.pkl & MLflow)       │
│                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                                                                
                                                                                                
┌────────────────────────────────────── INFERENCE FLOW (app.py /predict) ─────────────────────────────────┐
│                                                                                                         │
│  [ Upload CSV File ] ──► [ Load preprocessor.pkl ] ──► [ Load model.pkl ] ──► [ Interactive HTML table ]│
│                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

The project has been architected with high modularity and clean separation of concerns:

```text
network-security/
│
├── data_schema/
│   └── schema.yaml             # Defines features, expected data types, and target variable
│
├── networksecurity/            # Primary application codebase
│   ├── cloud/                  # Cloud synchronization utilities (S3 syncing capability)
│   ├── components/             # Concrete steps of the machine learning pipeline
│   │   ├── data_ingestion.py   # Database connection, retrieval, and splitting
│   │   ├── data_validation.py  # Schema matching & Kolmogorov-Smirnov drift validation
│   │   ├── data_transformation.py # Target normalization & KNN imputation execution
│   │   └── model_trainer.py    # Multi-model evaluation, tuning, and MLflow logging
│   │
│   ├── constant/               # Centralized configuration variables & hyperparameter grids
│   ├── entity/                 # Strongly typed Dataclasses defining configs and artifacts
│   ├── exception/              # Structured custom traceback exception wrapper
│   ├── logging/                # Timestamps and execution log managers
│   ├── pipeline/               # Orchestrates complete pipeline runs
│   └── utils/                  # Reusable auxiliary MLOps & math methods
│
├── final_model/                # Active production preprocessor and model artifacts
├── templates/                  # Frontend Jinja template folders
├── app.py                      # FastAPI microservice routing script
├── push_data.py                # Database population and ETL automation script
├── main.py                     # CLI pipeline initiator
├── requirements.txt            # Project environment dependency listings
└── README.md                   # Comprehensive technical documentation
```

---

## 🚀 Setup & Execution Guide

### 📋 Prerequisites
* Python 3.8, 3.9, or 3.10 installed on your system.
* A running MongoDB Atlas Instance (or local MongoDB).
* An MLflow/DagsHub account (Optional, can be modified in `.env`).

### 📦 1. Installation
Clone this repository to your workspace and navigate to its directory:

```bash
git clone https://github.com/<your-username>/networksecurity.git
cd networksecurity
```

Create and activate a isolated virtual environment:

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 🔑 2. Environment Configuration
Create a `.env` file in the root directory to store your credentials securely:

```env
MONGO_DB_URL="mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"
```

### 🗄️ 3. Seeding the Database
To upload raw network features from the CSV to your MongoDB Cluster, execute the ETL script:

```bash
python push_data.py
```

### 🖥️ 4. Running the Web Application
Start the FastAPI server via Uvicorn:

```bash
python app.py
```
*The service will start running at `http://localhost:8000`.*

---

## 🔌 API Endpoint Walkthrough

Once the FastAPI server is running, navigate to `http://localhost:8000` in your web browser. This redirects to the interactive **Swagger UI Documentation** (`/docs`):

### 1. Trigger Model Retraining (`GET /train`)
* **Endpoint:** `/train`
* **What it does:** Orchestrates a full execution of the pipeline. It queries MongoDB, validates data drift, handles missing values, optimizes models, logs runs to MLflow, and updates the local model artifacts.
* **Response:**
  ```text
  "Training successful"
  ```

### 2. Live Batch Prediction (`POST /predict`)
* **Endpoint:** `/predict`
* **What it does:** Accepts a `.csv` file containing the 30 schema features (excluding target). It instantly runs prediction and outputs a beautifully formatted HTML report displaying results directly on-screen.
* **Batch Save Output:** It also compiles and saves the full prediction CSV output inside `prediction_output/output.csv` on the host.

---

## 📊 Model Tuning & Performance Logs

The model training framework compares various classification algorithms. Below are example hyperparameters configured within `networksecurity/components/model_trainer.py` for automated GridSearch tuning:

| Model | Evaluated Hyperparameters |
| :--- | :--- |
| **Random Forest** | `n_estimators`: [8, 16, 32, 128, 256] |
| **Gradient Boosting** | `learning_rate`: [0.1, 0.01, 0.05, 0.001], `subsample`: [0.6, 0.7, 0.85, 0.9], `n_estimators`: [8, 16, 32, 64, 128, 256] |
| **AdaBoost** | `learning_rate`: [0.1, 0.01, 0.001], `n_estimators`: [8, 16, 32, 64, 128, 256] |
| **Decision Tree** | `criterion`: ['gini', 'entropy', 'log_loss'] |

### Experiment Tracking Screenshots (MLflow Dashboard)
All parameters and metrics are synchronized in real-time. This provides an elegant visualization dashboard where recruiters can observe model accuracy, precision, and AUC curves over time.

---

## 🌟 Highlights for Recruiters & Hiring Managers
* **Production-Ready Architecture:** Clean separation of concerns with dedicated `config_entity` and `artifact_entity` classes, simulating enterprise workflows.
* **Advanced MLOps:** Uses **MLflow** for experiment logging and model artifact version control.
* **Innovative Drift Detection:** Realized **dataset covariate drift validation** in software logic using Kolmogorov-Smirnov statistical tests.
* **Extensive Error Logging:** Includes robust logging structures and custom traceback handlers for prompt debugging.
* **Modern API Interface:** Implemented with **FastAPI** including robust asynchronous data uploads.

---

*Developed with passion for cybersecurity and machine learning. Feel free to connect, fork, or open a pull request!*
