# 🛡️ Fraud Detection AI System v3.0 (Full-Stack Edition)

An advanced, real-time fraud detection engine designed to identify and flag malicious conversational text. Originally built as a CLI tool, this project has evolved into a decoupled **Full-Stack Application** featuring a React.js frontend dashboard, a lightning-fast FastAPI backend, and a hybrid Machine Learning classification engine trained on real-world datasets.

## 🚀 Key Features

* **Hybrid Detection Architecture:** Combines rule-based heuristic scanning (regex pattern matching) with a probabilistic Machine Learning ensemble to minimize false positives and catch zero-day fraud attempts.
* **Full-Stack Web Dashboard:** A sleek, dark-mode React.js user interface that communicates seamlessly with the Python backend for real-time risk scoring.
* **Real-World Data Pipeline:** Includes a custom Pandas pipeline (`prepare_data.py`) to process, clean, and format the Kaggle SMS Spam Collection dataset, successfully handling imbalanced classes (747 Fraud vs. 4825 Normal).
* **Ensemble ML Model:** Utilizes a `VotingClassifier` blending Random Forest, Multinomial Naive Bayes, and Logistic Regression for highly accurate threat prediction.
* **FastAPI Microservice:** The ML engine is wrapped in a high-performance REST API, fully configured with CORS middleware for secure cross-origin requests.

## 🛠️ Technology Stack

**Frontend (The Face)**
* React.js (Vite)
* Custom CSS Dashboard

**Backend (The Bridge)**
* FastAPI
* Uvicorn (ASGI Web Server)
* Pydantic (Data Validation)

**Machine Learning (The Brain)**
* Python 3.x
* `scikit-learn` (Ensemble modeling, TF-IDF Vectorization)
* `pandas` & `numpy` (Data manipulation)

## 📦 Installation & Setup

Because this uses a decoupled full-stack architecture, you will need two separate terminal windows to run the frontend and backend servers simultaneously.

### Prerequisites
* Python 3.x installed
* Node.js and npm installed

###  Backend Setup (FastAPI & ML Engine)
Open your first terminal and clone the repository:
```bash
git clone [https://github.com/Akki-jaiswal/ai-fraud-detection-system.git](https://github.com/Akki-jaiswal/ai-fraud-detection-system.git)
cd ai-fraud-detection-system
