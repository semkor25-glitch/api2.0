from fastapi import FastAPI
from authmodel import AuthRiskModel, AuthRequest

app = FastAPI()
model = AuthRiskModel()

@app.get("/")
def root():
    return {"message": "Adaptive Authentication API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/risk")
def evaluate_risk(request: AuthRequest):
    risk = model.predict(
        request.hour, request.ip_risk, request.device_trust,
        request.geo_distance, request.fail_count, request.unusual_time,
        request.new_location, request.session_count
    )
    
    if risk == 0:
        decision = "allow"
        mfa = False
        msg = "✅ Доступ разрешен"
    elif risk == 1:
        decision = "mfa_required"
        mfa = True
        msg = "⚠️ Требуется MFA"
    else:
        decision = "blocked"
        mfa = False
        msg = "❌ Доступ блокирован"
    
    return {"risk_level": risk, "decision": decision, "mfa_required": mfa, "message": msg}

print("✅ API создан")
