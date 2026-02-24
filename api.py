from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Fraud_Detection_System import AdvancedFraudDetector, Config
import os
import uvicorn


app = FastAPI(title="Fraud Detection API", version="3.0")

# 1. BULLETPROOF CORS: Allows React to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading ML Model...")
detector = AdvancedFraudDetector()

class MessageRequest(BaseModel):
    text: str

# 2. EXACT ROUTE MATCH: Matches the React fetch request
@app.post("/analyze")
def analyze_text(req: MessageRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = detector.analyze(req.text)
    
    if not result:
        raise HTTPException(status_code=500, detail="Analysis failed")

    return {
        "text": result['text'],
        "risk_level": result['risk_level'],
        "risk_score": round(result['combined_score'], 2),
        "is_fraud": result['should_alert']
    }

# This tells the cloud provider to bind to the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)