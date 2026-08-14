from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from fraud_detector import analyse_content

from database import (
    initialize_database,
    save_scan,
    get_scan_history
)


app = FastAPI(
    title="SBI Sahayak AI",
    description=(
        "AI-powered banking assistance "
        "and fraud-awareness prototype"
    ),
    version="1.0.0"
)


# Allow frontend requests

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


initialize_database()


# -------------------------
# DATA MODELS
# -------------------------

class ChatRequest(BaseModel):

    message: str

    language: str = "English"


class ScanRequest(BaseModel):

    content: str


# -------------------------
# HOME
# -------------------------

@app.get("/")
def home():

    return {

        "project":
            "SBI Sahayak AI",

        "status":
            "online",

        "message":
            "Detect. Guide. Protect.",

        "version":
            "1.0"

    }


# -------------------------
# HEALTH
# -------------------------

@app.get("/api/health")
def health():

    return {

        "status": "healthy"

    }


# -------------------------
# CHAT
# -------------------------

@app.post("/api/chat")
def chat(request: ChatRequest):

    message =
        request.message.lower()


    # UPI

    if "upi" in message:

        if request.language == "ಕನ್ನಡ":

            response = (
                "UPI ಬಳಸುವಾಗ ನಿಮ್ಮ UPI PIN ಅಥವಾ OTP "
                "ಯಾರಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ. ಹಣ ಸ್ವೀಕರಿಸಲು "
                "PIN ನಮೂದಿಸುವ ಅಗತ್ಯವಿಲ್ಲ."
            )

        elif request.language == "हिन्दी":

            response = (
                "UPI का उपयोग करते समय अपना UPI PIN "
                "या OTP किसी के साथ साझा न करें। "
                "पैसे प्राप्त करने के लिए PIN की "
                "जरूरत नहीं होती।"
            )

        else:

            response = (
                "When using UPI, never share your "
                "UPI PIN or OTP. You do not need "
                "to enter your PIN to receive money."
            )


    # ATM

    elif "atm" in message:

        response = (
            "For ATM safety: cover the keypad "
            "while entering your PIN, never share "
            "your PIN, and collect your card before "
            "leaving the ATM."
        )


    # FRAUD

    elif (
        "scam" in message
        or "fraud" in message
        or "hack" in message
    ):

        response = (
            "Never share your OTP, PIN, CVV or "
            "password. Do not click suspicious "
            "links. If you receive a suspicious "
            "message, use the AI Scam Shield."
        )


    # INTERNET BANKING

    elif (
        "internet banking" in message
        or "online banking" in message
    ):

        response = (
            "Internet banking lets you securely "
            "manage eligible banking services "
            "online. Always access your bank "
            "through the official application "
            "or website."
        )


    # PASSWORD

    elif "password" in message:

        response = (
            "Use a strong, unique password and "
            "never share it with anyone. Avoid "
            "using your name, date of birth or "
            "mobile number."
        )


    # DEFAULT

    else:

        response = (
            "I can help you with UPI, ATM usage, "
            "internet banking, digital banking "
            "safety and scam awareness. Try asking "
            "a specific question."
        )


    return {

        "response": response,

        "language":
            request.language

    }


# -------------------------
# SCAM SCANNER
# -------------------------

@app.post("/api/scan")
def scan(request: ScanRequest):

    result =
        analyse_content(
            request.content
        )


    save_scan(

        request.content,

        result["risk_score"],

        result["risk_level"]

    )


    return result


# -------------------------
# HISTORY
# -------------------------

@app.get("/api/history")
def history():

    return {

        "results":
            get_scan_history()

    }


# -------------------------
# SERVER
# -------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )