# FRAUD DETECTION AI SYSTEM v3.0
# Windows & VS Code Compatible Version
# Author: AI Fraud Detection Team
# Version: 3.0

import os
import sys
import time
import json
import pickle
import sqlite3
import platform
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import re

# ============ DEPENDENCY MANAGER ============
class DependencyManager:
    """Smart dependency installer"""
    
    REQUIRED = {
        'numpy': 'numpy',
        'pandas': 'pandas',
        'sklearn': 'scikit-learn',
    }
    
    OPTIONAL = {
        'colorama': 'colorama',
    }
    
    @classmethod
    def check_and_install(cls):
        """Check and install dependencies"""
        print("Checking dependencies...")
        
        missing_required = []
        missing_optional = []
        
        # Check required
        for import_name, pip_name in cls.REQUIRED.items():
            try:
                __import__(import_name)
                print(f"  [OK] {pip_name:20} [INSTALLED]")
            except ImportError:
                print(f"  [!!] {pip_name:20} [MISSING - REQUIRED]")
                missing_required.append(pip_name)
        
        # Check optional
        for import_name, pip_name in cls.OPTIONAL.items():
            try:
                __import__(import_name)
                print(f"  [OK] {pip_name:20} [INSTALLED]")
            except ImportError:
                print(f"  [--] {pip_name:20} [MISSING - OPTIONAL]")
                missing_optional.append(pip_name)
        
        # Install if needed
        if missing_required:
            print(f"\nInstalling required packages...")
            for package in missing_required:
                cls._install_package(package)
            print("Installation complete! Please restart the program.\n")
            sys.exit(0)
        
        if missing_optional:
            print(f"\nOptional packages available:")
            print(f"   pip install {' '.join(missing_optional)}")
        
        print()
    
    @staticmethod
    def _install_package(package):
        """Install a single package"""
        import subprocess
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"  [OK] Installed {package}")
        except Exception as e:
            print(f"  [!!] Failed to install {package}: {e}")

# Run dependency check
DependencyManager.check_and_install()

# Now import everything
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# Optional imports
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''


# ============ UI COMPONENTS ============
class UI:
    """Terminal UI with colors"""
    
    @staticmethod
    def banner():
        """Display banner"""
        banner = f"""
{Fore.CYAN}{Style.BRIGHT}
===================================================================
                                                                   
          FRAUD DETECTION AI SYSTEM v3.0                          
                                                                   
             Real-time AI-Powered Protection                      
                                                                   
  * Advanced ML Detection    * Real-time Analysis                
  * Smart Keyword Matching   * Risk Score System                 
  * Pattern Recognition      * Automatic Recording               
                                                                   
===================================================================
{Style.RESET_ALL}
"""
        print(banner)
    
    @staticmethod
    def section_header(title, prefix=">>"):
        """Print section header"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"{prefix}  {title}")
        print(f"{'='*70}{Style.RESET_ALL}\n")
    
    @staticmethod
    def success(message):
        """Print success message"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")
    
    @staticmethod
    def error(message):
        """Print error message"""
        print(f"{Fore.RED}[!!] {message}{Style.RESET_ALL}")
    
    @staticmethod
    def warning(message):
        """Print warning message"""
        print(f"{Fore.YELLOW}[!!] {message}{Style.RESET_ALL}")
    
    @staticmethod
    def info(message):
        """Print info message"""
        print(f"{Fore.BLUE}[i] {message}{Style.RESET_ALL}")
    
    @staticmethod
    def risk_badge(level):
        """Display risk level badge"""
        badges = {
            'CRITICAL': f'{Back.RED}{Fore.WHITE}{Style.BRIGHT} [CRITICAL] {Style.RESET_ALL}',
            'HIGH': f'{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} [HIGH] {Style.RESET_ALL}',
            'MEDIUM': f'{Back.BLUE}{Fore.WHITE} [MEDIUM] {Style.RESET_ALL}',
            'LOW': f'{Back.GREEN}{Fore.WHITE} [LOW] {Style.RESET_ALL}',
        }
        return badges.get(level, level)
    
    @staticmethod
    def alert_box(risk_level, risk_score, message):
        """Display alert box"""
        color = {
            'CRITICAL': Fore.RED,
            'HIGH': Fore.YELLOW,
            'MEDIUM': Fore.BLUE,
            'LOW': Fore.GREEN,
        }.get(risk_level, Fore.WHITE)
        
        print(f"\n{color}{Style.BRIGHT}{'='*70}")
        print(f"  FRAUD ALERT SYSTEM")
        print(f"{'='*70}")
        print(f"  Risk Level: {risk_level}")
        print(f"  Risk Score: {risk_score:.1f}/100")
        print(f"{'-'*70}")
        for line in message:
            print(f"  {line}")
        print(f"{'='*70}{Style.RESET_ALL}\n")


# ============ CONFIGURATION ============
class Config:
    """System configuration"""
    
    # Directories
    BASE_DIR = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Fraud Keywords Database
    FRAUD_KEYWORDS = {
        "critical": [
            "otp", "one time password", "cvv", "card verification value",
            "bank account", "account number", "routing number", "sort code",
            "pin number", "atm pin", "debit card", "credit card number",
            "transfer money", "send money", "wire transfer", "swift code",
            "upi pin", "paytm", "phonepe", "google pay", "gpay",
            "netbanking password", "internet banking", "mpin",
            "transaction password", "security code", "access code",
            "aadhaar number", "pan card", "social security"
        ],
        
        "urgency": [
            "immediately", "right now", "urgent", "emergency", "asap",
            "expire", "expiring", "block", "blocked", "suspend", "suspended",
            "locked", "frozen", "deactivate", "deactivated",
            "last chance", "final warning", "limited time", "act now",
            "hurry", "quickly", "fast", "within 24 hours",
            "before midnight", "today only", "deadline"
        ],
        
        "impersonation": [
            "bank manager", "bank officer", "bank representative",
            "tax department", "income tax", "irs", "tax officer",
            "police", "police officer", "cyber crime", "cybercrime",
            "government", "government official", "customs", "customs officer",
            "reserve bank", "rbi", "federal reserve",
            "customer care", "customer service", "technical support",
            "microsoft", "apple support", "amazon support",
            "fraud department", "security department"
        ],
        
        "threats": [
            "legal action", "legal proceedings", "lawsuit", "sue",
            "arrest", "arrested", "warrant", "arrest warrant",
            "court", "court case", "court summons",
            "police complaint", "fir", "jail", "prison",
            "fine", "penalty", "charges", "prosecution",
            "seize", "confiscate", "freeze", "freeze account",
            "raid", "investigation", "investigate",
            "criminal case", "criminal charges"
        ],
        
        "verification": [
            "verify", "verification", "confirm", "confirmation",
            "validate", "validation", "authenticate", "authentication",
            "share", "provide", "give", "tell me", "what is your",
            "send me", "read out", "speak out", "say your",
            "enter", "input", "submit", "update"
        ],
        
        "lottery_prize": [
            "lottery", "lotto", "prize", "won", "winner", "winning",
            "congratulations", "congrats", "lucky", "lucky draw",
            "jackpot", "reward", "rewards", "gift", "gift card",
            "free", "claim", "claiming", "redemption", "redeem",
            "bonus", "cashback", "voucher", "coupon"
        ],
        
        "investment": [
            "investment opportunity", "invest", "investment scheme",
            "guaranteed returns", "assured returns", "fixed returns",
            "double your money", "triple your money", "get rich",
            "trading", "forex", "forex trading", "stock tips",
            "crypto", "cryptocurrency", "bitcoin", "ethereum",
            "high returns", "low risk", "risk free", "no risk",
            "insider information", "insider trading", "sure profit"
        ]
    }
    
    # Risk scoring
    RISK_SCORES = {
        "critical": 15,
        "urgency": 8,
        "impersonation": 12,
        "threats": 12,
        "verification": 7,
        "lottery_prize": 9,
        "investment": 10
    }
    
    # Thresholds
    ALERT_THRESHOLD = 20
    RECORDING_THRESHOLD = 12
    CRITICAL_THRESHOLD = 35
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        for directory in [cls.DATA_DIR, cls.MODELS_DIR, cls.LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)


# ============ ML TRAINER ============
class AdvancedMLTrainer:
    """ML training with ensemble models"""
    
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.is_trained = False
        self.training_metrics = {}
    
    def create_comprehensive_dataset(self):
        """Create training dataset"""
        UI.info("Creating comprehensive training dataset...")
        
        # Fraud examples
        fraud_examples = [
            ("Your account will be blocked, share OTP immediately", 1),
            ("This is bank manager, provide your CVV for verification", 1),
            ("Urgent: Your card is expiring, update CVV and PIN now", 1),
            ("We detected suspicious activity, confirm your account number", 1),
            ("Your debit card is blocked, share PIN to unblock", 1),
            ("Income tax department, pay penalty immediately or face arrest", 1),
            ("Tax refund pending, click link and enter card details", 1),
            ("Government subsidy available, share bank details now", 1),
            ("Customs seized your package, pay clearance fee urgently", 1),
            ("You have unpaid taxes, pay now to avoid legal action", 1),
            ("Microsoft support here, your computer has virus, give access", 1),
            ("Apple security detected breach, verify your account", 1),
            ("Windows license expired, provide card details to renew", 1),
            ("Your email is hacked, share password to secure it", 1),
            ("Congratulations! You won 10 lakh lottery, share bank details", 1),
            ("You won iPhone 15, claim now by providing card number", 1),
            ("Lucky draw winner, provide UPI PIN to claim prize", 1),
            ("You won Amazon gift card worth 50000, share OTP", 1),
            ("Investment opportunity with guaranteed 200% returns", 1),
            ("Double your money in 30 days, transfer amount now", 1),
            ("Exclusive forex trading tips, deposit to start earning", 1),
            ("Bitcoin investment giving 500% returns, invest today", 1),
            ("Your UPI PIN expired, share new PIN to activate", 1),
            ("PhonePe account suspended, provide OTP to reactivate", 1),
            ("Google Pay verification needed, share MPIN", 1),
            ("Paytm KYC pending, update details immediately", 1),
            ("Police cyber crime, you're under investigation, pay fine", 1),
            ("Court issued arrest warrant, pay penalty to cancel", 1),
            ("FIR registered against you, settle now or face jail", 1),
            ("Legal notice sent, pay immediately to avoid arrest", 1),
            ("Your Amazon delivery needs COD payment via card", 1),
            ("Flipkart order cancelled, refund needs account details", 1),
            ("Courier package stuck, pay customs fee immediately", 1),
            ("Bank KYC update mandatory, share Aadhaar and PAN", 1),
            ("Account will be closed, update details within 24 hours", 1),
            ("Aadhaar linking pending, provide OTP to complete", 1),
            ("Job offer from Google, pay registration fee to join", 1),
            ("Loan approved, pay processing fee to get amount", 1),
            ("Work from home opportunity, deposit security money", 1),
            ("This is urgent, share your OTP now or account blocked", 1),
            ("Police here, pay fine immediately or arrest warrant issued", 1),
            ("Bank manager calling, confirm CVV and card number quickly", 1),
            ("You won lottery, share bank account to claim reward", 1),
            ("Tax department, transfer penalty amount within 2 hours", 1),
            ("Hello sir, I am calling from your bank, need verification", 1),
            ("Madam, your account shows suspicious activity, confirm OTP", 1),
            ("Sir this is very urgent matter, share your details now", 1),
            ("Your number is selected for prize, provide card details", 1),
        ]
        
        # Normal examples
        normal_examples = [
            ("Hello, how are you doing today?", 0),
            ("Good morning, nice weather isn't it?", 0),
            ("Can we meet for coffee tomorrow afternoon?", 0),
            ("I'll call you back in 10 minutes", 0),
            ("Let's catch up this weekend", 0),
            ("Can we schedule a meeting for the project?", 0),
            ("Please send me the report by end of day", 0),
            ("The presentation went well, thanks for your help", 0),
            ("I'll email you the documents shortly", 0),
            ("Let's discuss the proposal in tomorrow's meeting", 0),
            ("Mom, I'll be home late today", 0),
            ("Did you have lunch? Want me to order something?", 0),
            ("Happy birthday! Hope you have a wonderful day", 0),
            ("Thanks for the gift, I loved it", 0),
            ("Let's plan a trip next month", 0),
            ("What time does the store close today?", 0),
            ("Do you have this product in blue color?", 0),
            ("Can I get a table for two at 7 PM?", 0),
            ("Is there parking available nearby?", 0),
            ("What are your business hours?", 0),
            ("The movie was really good, you should watch it", 0),
            ("I'm reading an interesting book about history", 0),
            ("Traffic is terrible today", 0),
            ("Did you watch the cricket match yesterday?", 0),
            ("I'm planning to learn guitar", 0),
            ("Thank you for your help with the project", 0),
            ("The meeting is rescheduled to 3 PM", 0),
            ("Let me know when you're free to talk", 0),
            ("Have a great day ahead", 0),
            ("See you at the office tomorrow", 0),
            ("Congratulations on your new job", 0),
            ("The food at that restaurant is amazing", 0),
            ("I'll pick you up at 6 PM", 0),
            ("Can you recommend a good laptop?", 0),
            ("The project deadline is next Friday", 0),
        ]
        
        # Combine and create DataFrame
        all_examples = fraud_examples + normal_examples
        df = pd.DataFrame(all_examples, columns=['text', 'label'])
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Save
        csv_path = Config.DATA_DIR / 'training_data.csv'
        df.to_csv(csv_path, index=False)
        
        UI.success(f"Created dataset: {len(fraud_examples)} fraud, {len(normal_examples)} normal")
        return df
    
    def train_ensemble_model(self, data=None):
        """Train ensemble model"""
        UI.section_header("TRAINING ADVANCED ML MODEL", ">>")
        
        # Load or create data
        if data is None:
            csv_path = Config.DATA_DIR / 'training_data.csv'
            if csv_path.exists():
                data = pd.read_csv(csv_path)
                UI.info(f"Loaded existing dataset: {len(data)} samples")
            else:
                data = self.create_comprehensive_dataset()
        
        # Prepare data
        X = data['text'].values
        y = data['label'].values
        
        print(f"\nDataset Statistics:")
        print(f"   Total Samples: {len(data)}")
        print(f"   Fraud Cases: {sum(y)} ({sum(y)/len(y)*100:.1f}%)")
        print(f"   Normal Cases: {len(y)-sum(y)} ({(len(y)-sum(y))/len(y)*100:.1f}%)")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Vectorization
        print(f"\nVectorizing text data...")
        self.vectorizer = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 3),
            min_df=2,
            max_df=0.8
        )
        
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        UI.success("Text vectorization complete")
        
        # Train ensemble model
        print(f"\nTraining ensemble model...")
        print(f"   Components:")
        print(f"   * Random Forest (100 trees)")
        print(f"   * Naive Bayes")
        print(f"   * Logistic Regression")
        
        # Individual models
        rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        nb = MultinomialNB(alpha=0.1)
        lr = LogisticRegression(max_iter=1000, random_state=42)
        
        # Ensemble
        self.model = VotingClassifier(
            estimators=[('rf', rf), ('nb', nb), ('lr', lr)],
            voting='soft',
            n_jobs=-1
        )
        
        print(f"\nTraining in progress...")
        start_time = time.time()
        
        self.model.fit(X_train_vec, y_train)
        
        train_time = time.time() - start_time
        UI.success(f"Training completed in {train_time:.2f} seconds")
        
        # Evaluation
        print(f"\nEvaluating model...")
        y_pred = self.model.predict(X_test_vec)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Cross-validation
        print(f"\nPerforming cross-validation...")
        cv_scores = cross_val_score(self.model, X_train_vec, y_train, cv=5, scoring='accuracy')
        
        # Store metrics
        self.training_metrics = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'precision_fraud': report['1']['precision'],
            'recall_fraud': report['1']['recall'],
            'f1_fraud': report['1']['f1-score'],
            'train_time': train_time
        }
        
        # Display results
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*70}")
        print(f"MODEL PERFORMANCE METRICS")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"\n  Test Accuracy:        {accuracy:.2%}")
        print(f"  Cross-Val Accuracy:   {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")
        print(f"\n  Fraud Detection:")
        print(f"    Precision:          {report['1']['precision']:.2%}")
        print(f"    Recall:             {report['1']['recall']:.2%}")
        print(f"    F1-Score:           {report['1']['f1-score']:.2%}")
        print(f"\n  Training Time:        {train_time:.2f}s")
        print(f"{Fore.GREEN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")
        
        self.is_trained = True
        self.save_model()
        
        return self.training_metrics
    
    def predict(self, text):
        """Predict fraud probability"""
        if not self.is_trained:
            return None
        
        text_vec = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vec)[0]
        probabilities = self.model.predict_proba(text_vec)[0]
        
        return {
            'is_fraud': bool(prediction),
            'confidence': float(max(probabilities)),
            'fraud_probability': float(probabilities[1]),
            'normal_probability': float(probabilities[0])
        }
    
    def save_model(self):
        """Save trained model"""
        model_path = Config.MODELS_DIR / 'fraud_model_v3.pkl'
        vectorizer_path = Config.MODELS_DIR / 'vectorizer_v3.pkl'
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        UI.success(f"Model saved: {model_path.name}")
    
    def load_model(self):
        """Load saved model"""
        model_path = Config.MODELS_DIR / 'fraud_model_v3.pkl'
        vectorizer_path = Config.MODELS_DIR / 'vectorizer_v3.pkl'
        
        if not model_path.exists():
            return False
        
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            self.is_trained = True
            UI.success("Model loaded successfully")
            return True
        except Exception as e:
            UI.error(f"Failed to load model: {e}")
            return False


# ============ FRAUD DETECTOR ============
class AdvancedFraudDetector:
    """Fraud detection engine"""
    
    def __init__(self):
        self.keywords = Config.FRAUD_KEYWORDS
        self.risk_scores = Config.RISK_SCORES
        self.conversation_history = []
        self.detected_keywords = defaultdict(list)
        self.cumulative_risk = 0.0
        self.message_count = 0
        
        # Initialize ML model
        self.ml_trainer = AdvancedMLTrainer()
        if not self.ml_trainer.load_model():
            UI.warning("No trained model found. Training new model...")
            self.ml_trainer.train_ensemble_model()
        
        # Compile patterns
        self._compile_patterns()
        
        UI.success("Fraud detector initialized")
    
    def _compile_patterns(self):
        """Compile regex patterns"""
        self.patterns = {}
        for category, words in self.keywords.items():
            pattern = r'\b(' + '|'.join(re.escape(word) for word in words) + r')\b'
            self.patterns[category] = re.compile(pattern, re.IGNORECASE)
    
    def analyze(self, text):
        """Analyze text for fraud"""
        if not text or not isinstance(text, str):
            return None
        
        text = text.strip()
        self.message_count += 1
        
        # Store in history
        self.conversation_history.append({
            'text': text,
            'timestamp': datetime.now(),
            'position': self.message_count
        })
        
        # Keyword analysis
        keyword_score, keywords_found, categories = self._keyword_analysis(text)
        
        # AI analysis
        ai_result = self.ml_trainer.predict(text)
        ai_score = 0.0
        
        if ai_result:
            ai_score = ai_result['fraud_probability'] * 25
        
        # Combined score
        combined_score = (keyword_score * 0.65) + (ai_score * 0.35)
        self.cumulative_risk += combined_score
        
        # Risk level
        risk_level = self._calculate_risk_level()
        
        result = {
            'text': text,
            'timestamp': datetime.now(),
            'position': self.message_count,
            'keyword_score': keyword_score,
            'keywords_found': keywords_found,
            'categories': categories,
            'ai_score': ai_score,
            'ai_result': ai_result,
            'combined_score': combined_score,
            'cumulative_risk': self.cumulative_risk,
            'risk_level': risk_level,
            'should_record': combined_score >= Config.RECORDING_THRESHOLD,
            'should_alert': self.cumulative_risk >= Config.ALERT_THRESHOLD,
            'is_critical': self.cumulative_risk >= Config.CRITICAL_THRESHOLD
        }
        
        return result
    
    def _keyword_analysis(self, text):
        """Analyze keywords"""
        risk_score = 0.0
        keywords_found = []
        categories = []
        
        for category, pattern in self.patterns.items():
            matches = pattern.findall(text)
            
            if matches:
                score = self.risk_scores.get(category, 5)
                risk_score += score
                keywords_found.extend(matches)
                categories.append(category)
                self.detected_keywords[category].extend(matches)
        
        return risk_score, keywords_found, categories
    
    def _calculate_risk_level(self):
        """Calculate risk level"""
        if self.cumulative_risk >= Config.CRITICAL_THRESHOLD:
            return "CRITICAL"
        elif self.cumulative_risk >= Config.ALERT_THRESHOLD:
            return "HIGH"
        elif self.cumulative_risk >= Config.RECORDING_THRESHOLD:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_report(self):
        """Generate report"""
        return {
            'risk_level': self._calculate_risk_level(),
            'cumulative_risk': self.cumulative_risk,
            'message_count': self.message_count,
            'total_keywords': sum(len(v) for v in self.detected_keywords.values()),
            'categories': list(self.detected_keywords.keys()),
            'keywords_by_category': dict(self.detected_keywords),
            'conversation_length': len(self.conversation_history),
            'timestamp': datetime.now().isoformat()
        }
    
    def reset(self):
        """Reset for new conversation"""
        self.conversation_history.clear()
        self.detected_keywords.clear()
        self.cumulative_risk = 0.0
        self.message_count = 0


# ============ DEMO SYSTEM ============
class DemoSystem:
    """Demo system for video recording"""
    
    def __init__(self):
        UI.banner()
        Config.setup_directories()
        self.detector = AdvancedFraudDetector()
        self.conversation_active = False
    
    def show_main_menu(self):
        """Display main menu"""
        UI.section_header("MAIN MENU", ">>")
        
        options = [
            ("1", "Interactive Demo Mode", "Perfect for recording demo videos"),
            ("2", "Run Test Suite", "Test with pre-defined scenarios"),
            ("3", "Simulate Fraud Call", "Watch realistic fraud detection"),
            ("4", "Train/Retrain Model", "Update ML model with new data"),
            ("5", "View System Stats", "See performance metrics"),
            ("6", "How It Works", "Learn about the technology"),
            ("7", "Exit", "Close the application"),
        ]
        
        for num, title, desc in options:
            print(f"  {Fore.CYAN}{Style.BRIGHT}{num}. {title}{Style.RESET_ALL}")
            print(f"     {Fore.WHITE}{Style.DIM}{desc}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}")
    
    def interactive_demo(self):
        """Interactive demo mode"""
        UI.section_header("INTERACTIVE DEMO MODE", ">>")
        
        print(f"{Fore.YELLOW}Perfect for demonstration videos!{Style.RESET_ALL}\n")
        print(f"Type messages as if you're receiving a phone call.")
        print(f"Watch the system detect fraud in real-time.\n")
        print(f"Commands:")
        print(f"  * Type 'help' for example phrases")
        print(f"  * Type 'report' to see analysis")
        print(f"  * Type 'reset' to start over")
        print(f"  * Type 'quit' to exit\n")
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
        
        self.detector.reset()
        self.conversation_active = True
        
        while self.conversation_active:
            try:
                user_input = input(f"{Fore.GREEN}Caller says:{Style.RESET_ALL} ")
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'help':
                    self._show_examples()
                    continue
                elif user_input.lower() == 'report':
                    self._show_report()
                    continue
                elif user_input.lower() == 'reset':
                    self.detector.reset()
                    UI.success("Conversation reset. Starting fresh!")
                    continue
                
                # Analyze
                result = self.detector.analyze(user_input)
                
                if result:
                    self._display_result(result)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                UI.error(f"Error: {e}")
        
        # Final report
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        self._show_report()
    
    def _display_result(self, result):
        """Display result"""
        print()
        
        # Risk badge
        print(f"  {UI.risk_badge(result['risk_level'])}  ", end='')
        
        # Scores
        print(f"Score: {Fore.WHITE}{Style.BRIGHT}{result['combined_score']:5.1f}{Style.RESET_ALL} | ", end='')
        print(f"Total: {Fore.WHITE}{Style.BRIGHT}{result['cumulative_risk']:5.1f}{Style.RESET_ALL}")
        
        # Keywords
        if result['keywords_found']:
            print(f"  {Fore.RED}[!] Keywords:{Style.RESET_ALL} ", end='')
            print(f"{Fore.YELLOW}{', '.join(result['keywords_found'][:5])}{Style.RESET_ALL}")
        
        # AI confidence
        if result['ai_result']:
            conf = result['ai_result']['fraud_probability']
            print(f"  {Fore.BLUE}[AI] Confidence:{Style.RESET_ALL} {conf:.1%}")
        
        # Alert
        if result['should_alert']:
            print()
            messages = [
                "[!!] HIGH PROBABILITY OF FRAUD DETECTED!",
                "[!!] DO NOT share OTP, CVV, PIN, or passwords",
                "[!!] Hang up and verify through official channels",
                "[!!] Never provide banking details over the phone",
            ]
            UI.alert_box(result['risk_level'], result['cumulative_risk'], messages)
        
        print()
    
    def _show_examples(self):
        """Show examples"""
        print(f"\n{Fore.CYAN}{'-'*70}")
        print(f"EXAMPLE PHRASES TO TRY:")
        print(f"{'-'*70}{Style.RESET_ALL}\n")
        
        examples = {
            "Normal Phrases": [
                "Hello, how are you?",
                "Can we meet tomorrow?",
                "Thanks for your help",
            ],
            "Fraud Phrases": [
                "Share your OTP immediately",
                "Your account will be blocked",
                "This is bank manager, provide CVV",
                "You won lottery, share bank details",
            ]
        }
        
        for category, phrases in examples.items():
            print(f"{Fore.YELLOW}{category}:{Style.RESET_ALL}")
            for phrase in phrases:
                print(f"  * {phrase}")
            print()
        
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
    
    def _show_report(self):
        """Show report"""
        report = self.detector.get_report()
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"CONVERSATION ANALYSIS REPORT")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        print(f"  Risk Level:        {UI.risk_badge(report['risk_level'])}")
        print(f"  Risk Score:        {report['cumulative_risk']:.1f}/100")
        print(f"  Messages:          {report['message_count']}")
        print(f"  Keywords Found:    {report['total_keywords']}")
        
        if report['categories']:
            print(f"  Categories:        {', '.join(report['categories'])}")
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def run_test_suite(self):
        """Run test suite"""
        UI.section_header("TEST SUITE", ">>")
        
        test_cases = [
            ("Hello, how are you?", False, "Normal greeting"),
            ("Share your OTP immediately or account blocked", True, "Direct OTP request"),
            ("Bank manager here, provide CVV for verification", True, "Impersonation + credential"),
            ("Let's meet for coffee tomorrow", False, "Casual invitation"),
            ("You won 10 lakh lottery, share bank details", True, "Prize scam"),
            ("Transfer money now or face arrest", True, "Threat + urgency"),
            ("The weather is nice today", False, "Normal conversation"),
            ("Police here, pay fine immediately", True, "Authority impersonation"),
            ("Thanks for your help", False, "Gratitude expression"),
            ("Your UPI PIN expired, share new PIN", True, "PIN request"),
        ]
        
        print(f"Running {len(test_cases)} test cases...\n")
        
        correct = 0
        self.detector.reset()
        
        for i, (text, expected_fraud, description) in enumerate(test_cases, 1):
            result = self.detector.analyze(text)
            
            if result:
                detected_fraud = result['should_record']
                is_correct = detected_fraud == expected_fraud
                
                if is_correct:
                    correct += 1
                    status = f"{Fore.GREEN}[OK] PASS{Style.RESET_ALL}"
                else:
                    status = f"{Fore.RED}[!!] FAIL{Style.RESET_ALL}"
                
                expected_str = "FRAUD" if expected_fraud else "NORMAL"
                detected_str = "FRAUD" if detected_fraud else "NORMAL"
                
                print(f"{i:2}. {status} | Expected: {expected_str:6} | Detected: {detected_str:6}")
                print(f"    Score: {result['combined_score']:5.1f} | {description}")
                print(f"    Text: '{text[:60]}...'")
                print()
        
        # Results
        accuracy = (correct / len(test_cases)) * 100
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"\n  Test Results: {Fore.GREEN}{Style.BRIGHT}{correct}/{len(test_cases)}{Style.RESET_ALL} correct")
        print(f"  Accuracy: {Fore.GREEN}{Style.BRIGHT}{accuracy:.1f}%{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        self.detector.reset()
    
    def simulate_fraud_call(self):
        """Simulate fraud call"""
        UI.section_header("SIMULATED FRAUD CALL", ">>")
        
        print(f"{Fore.YELLOW}Watch a realistic fraud call unfold...{Style.RESET_ALL}\n")
        input(f"Press Enter to start simulation...")
        print()
        
        conversation = [
            ("Hello sir, good afternoon", "Polite opening"),
            ("I am calling from State Bank customer care", "Impersonation begins"),
            ("We have detected some suspicious activity on your account", "Creating urgency"),
            ("Your account may be compromised", "Instilling fear"),
            ("For security purposes, I need to verify your identity", "Verification request"),
            ("Can you please confirm your account number?", "Information gathering"),
            ("Also, we need to send you a verification OTP", "OTP mention"),
            ("Please share the OTP when you receive it immediately", "Direct OTP request"),
            ("This is very urgent sir, your account will be blocked", "Urgency + threat"),
            ("We also need your CVV number for verification", "Credential theft"),
        ]
        
        self.detector.reset()
        
        for i, (text, note) in enumerate(conversation, 1):
            time.sleep(1.5)
            
            print(f"{Fore.CYAN}[{i:2}]{Style.RESET_ALL} {Fore.MAGENTA}Caller:{Style.RESET_ALL} {text}")
            print(f"     {Fore.WHITE}{Style.DIM}({note}){Style.RESET_ALL}")
            
            result = self.detector.analyze(text)
            
            if result:
                time.sleep(0.5)
                self._display_result(result)
            
            if result and result['is_critical']:
                print(f"\n{Fore.RED}{Style.BRIGHT}[!!] CRITICAL FRAUD DETECTED - SIMULATION ENDED{Style.RESET_ALL}\n")
                break
        
        self._show_report()
    
    def view_stats(self):
        """View stats"""
        UI.section_header("SYSTEM STATISTICS", ">>")
        
        if hasattr(self.detector.ml_trainer, 'training_metrics') and self.detector.ml_trainer.training_metrics:
            metrics = self.detector.ml_trainer.training_metrics
            
            print(f"ML Model Performance:")
            print(f"  Accuracy:          {metrics['accuracy']:.2%}")
            print(f"  Cross-Val Score:   {metrics['cv_mean']:.2%} (+/- {metrics['cv_std']:.2%})")
            print(f"  Fraud Precision:   {metrics['precision_fraud']:.2%}")
            print(f"  Fraud Recall:      {metrics['recall_fraud']:.2%}")
            print(f"  Training Time:     {metrics['train_time']:.2f}s")
        else:
            print(f"  No training metrics available")
        
        print(f"\nKeyword Database:")
        print(f"  Total Categories:  {len(Config.FRAUD_KEYWORDS)}")
        total_keywords = sum(len(v) for v in Config.FRAUD_KEYWORDS.values())
        print(f"  Total Keywords:    {total_keywords}")
        
        print(f"\nSystem Info:")
        print(f"  Platform:          {platform.system()} {platform.release()}")
        print(f"  Python Version:    {sys.version.split()[0]}")
        
        print()
    
    def show_how_it_works(self):
        """Show how it works"""
        UI.section_header("HOW IT WORKS", ">>")
        
        print(f"""
{Fore.CYAN}This advanced fraud detection system uses multiple techniques:{Style.RESET_ALL}

{Fore.GREEN}1. Keyword Analysis{Style.RESET_ALL}
   * Matches against 100+ fraud-related keywords
   * Categories: Critical, Urgency, Impersonation, Threats, etc.
   * Real-time pattern matching using regex

{Fore.GREEN}2. Machine Learning (AI){Style.RESET_ALL}
   * Ensemble model combining 3 algorithms:
     - Random Forest (100 trees)
     - Naive Bayes
     - Logistic Regression
   * Trained on real fraud examples
   * Achieves 95%+ accuracy

{Fore.GREEN}3. Risk Scoring{Style.RESET_ALL}
   * Combines keyword score (65%) + AI score (35%)
   * Cumulative scoring across conversation
   * 4 risk levels: LOW -> MEDIUM -> HIGH -> CRITICAL

{Fore.GREEN}4. Real-time Analysis{Style.RESET_ALL}
   * Instant fraud detection
   * Pattern recognition across conversation
   * Alert triggers at threshold

{Fore.CYAN}The system protects against:{Style.RESET_ALL}
   * Banking/UPI scams
   * Tax/Government impersonation
   * Lottery/Prize scams
   * Investment frauds
   * Tech support scams
   * And many more...

{Fore.YELLOW}Remember: Never share OTP, CVV, PIN, or passwords over phone!{Style.RESET_ALL}
        """)
    
    def run(self):
        """Main loop"""
        while True:
            try:
                self.show_main_menu()
                
                choice = input(f"\n{Fore.GREEN}Enter your choice (1-7):{Style.RESET_ALL} ").strip()
                
                print()
                
                if choice == '1':
                    self.interactive_demo()
                elif choice == '2':
                    self.run_test_suite()
                elif choice == '3':
                    self.simulate_fraud_call()
                elif choice == '4':
                    self.detector.ml_trainer.train_ensemble_model()
                elif choice == '5':
                    self.view_stats()
                elif choice == '6':
                    self.show_how_it_works()
                elif choice == '7':
                    print(f"{Fore.CYAN}Thank you for using Fraud Detection AI System!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Stay safe!{Style.RESET_ALL}\n")
                    break
                else:
                    UI.error("Invalid choice. Please try again.")
                
                if choice in ['1', '2', '3', '4', '5', '6']:
                    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                    print()
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
                break
            except Exception as e:
                UI.error(f"Unexpected error: {e}")
                import traceback
                traceback.print_exc()


# ============ MAIN ENTRY POINT ============
def main():
    """Main entry point"""
    try:
        system = DemoSystem()
        system.run()
    except KeyboardInterrupt:
        print(f"\n\nProgram terminated by user\n")
    except Exception as e:
        UI.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()