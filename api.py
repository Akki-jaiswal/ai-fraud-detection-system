from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Fraud_Detection_System import AdvancedFraudDetector

# Initialize API and Detector
app = FastAPI(
    title="Fraud Detection AI API",
    description="Real-time hybrid fraud detection engine",
    version="3.0"
)

# Load the model once when the server starts
print("Loading ML Model...")
detector = AdvancedFraudDetector()

# Define what the incoming JSON request should look like
class MessageRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    """Simple health check endpoint"""
    return {
        "status": "online", 
        "message": "Fraud Detection API v3.0 is running. Go to /docs to test it!"
    }

@app.post("/api/v1/analyze")
def analyze_text(req: MessageRequest):
    """Analyze a text message for fraud indicators"""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Run text through your existing hybrid engine
    result = detector.analyze(req.text)
    
    if not result:
        raise HTTPException(status_code=500, detail="Analysis failed")

    # Format and return the JSON response
    return {
        "text": result['text'],
        "risk_level": result['risk_level'],
        "risk_score": round(result['combined_score'], 2),
        "is_fraud": result['should_alert'],
        "keywords_found": result['keywords_found'],
        "ai_fraud_probability": round(result['ai_result']['fraud_probability'] * 100, 2) if result['ai_result'] else 0.0
    }