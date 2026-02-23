# 🛡️ Fraud Detection AI System v3.0

An advanced, real-time fraud detection engine designed to identify and flag malicious conversational text. This system utilizes a **Hybrid Detection Architecture**, combining high-speed heuristic keyword scanning with a probabilistic Machine Learning ensemble to deliver highly accurate risk scoring.

## 🚀 System Architecture

This project moves beyond simple keyword matching by implementing a dual-engine analysis pipeline.

### 1. The Hybrid Detection Engine (`AdvancedFraudDetector`)
To minimize false positives while catching zero-day fraud attempts, the system scores text using two parallel engines:

* **Heuristic Engine (65% Weight):** Uses optimized Regular Expressions to scan for over 100+ critical threat indicators across 7 categories (e.g., Urgency, Impersonation, Credential Theft). It assigns weighted penalties based on the severity of the flagged keywords.
* **AI/ML Engine (35% Weight):** Processes the semantic structure of the sentence to predict the probability of fraud, catching nuanced scams that avoid trigger words.

**Cumulative Risk Scoring:** The system tracks state across a conversation. It aggregates the hybrid scores from each message to determine the overall conversational risk, escalating through four levels: `LOW` ➔ `MEDIUM` ➔ `HIGH` ➔ `CRITICAL`.

### 2. The Machine Learning Core (`AdvancedMLTrainer`)
The predictive backbone of the system is an ensemble Machine Learning model built with `scikit-learn`. 

* **Text Vectorization:** Converts raw conversational text into a numerical matrix using `TfidfVectorizer`. It captures unigrams, bigrams, and trigrams (up to 3-word phrases) to understand context (e.g., distinguishing between "bank on it" and "bank account").
* **Ensemble Voting Classifier:** Instead of relying on a single algorithm, the model uses a soft-voting mechanism that averages the probabilistic outputs of three distinct classifiers:
  1. **Random Forest (100 estimators):** Excellent at handling non-linear relationships and complex decision boundaries.
  2. **Multinomial Naive Bayes:** Highly effective and computationally lightweight for text classification and spam detection.
  3. **Logistic Regression:** Provides a strong baseline for binary classification (Fraud vs. Normal) with well-calibrated probabilities.

## 🛠️ Technology Stack

* **Language:** Python 3.x
* **Machine Learning:** `scikit-learn`
* **Data Processing:** `pandas`, `numpy`
* **UI/Console:** `colorama` (for risk-level color mapping)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Akki-jaiswal/ai-fraud-detection-system.git](https://github.com/Akki-jaiswal/ai-fraud-detection-system.git)
   cd ai-fraud-detection-system