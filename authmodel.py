import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from pydantic import BaseModel
import joblib

class AuthRequest(BaseModel):
    hour: int
    ip_risk: int
    device_trust: int
    geo_distance: int
    fail_count: int
    unusual_time: int
    new_location: int
    session_count: int

class AuthRiskModel:
    def __init__(self):
        np.random.seed(42)
        
        # Нормальные данные (500)
        normal = pd.DataFrame({
            'hour': np.random.randint(9, 17, 500),
            'ip_risk': np.random.randint(0, 3, 500),
            'device_trust': np.random.randint(70, 100, 500),
            'geo_distance': np.random.randint(0, 50, 500),
            'fail_count': np.random.randint(0, 1, 500),
            'unusual_time': [0]*500,
            'new_location': [0]*500,
            'session_count': np.random.randint(1, 3, 500)
        })
        
        # Средний риск (300)
        medium = pd.DataFrame({
            'hour': np.random.randint(6, 23, 300),
            'ip_risk': np.random.randint(3, 7, 300),
            'device_trust': np.random.randint(30, 70, 300),
            'geo_distance': np.random.randint(50, 200, 300),
            'fail_count': np.random.randint(1, 3, 300),
            'unusual_time': np.random.randint(0, 2, 300),
            'new_location': np.random.randint(0, 2, 300),
            'session_count': np.random.randint(1, 4, 300)
        })
        
        # Высокий риск (200)
        high = pd.DataFrame({
            'hour': np.random.randint(0, 24, 200),
            'ip_risk': np.random.randint(5, 10, 200),
            'device_trust': np.random.randint(0, 40, 200),
            'geo_distance': np.random.randint(200, 1000, 200),
            'fail_count': np.random.randint(2, 5, 200),
            'unusual_time': np.random.randint(0, 2, 200),
            'new_location': np.random.randint(0, 2, 200),
            'session_count': np.random.randint(0, 2, 200)
        })
        
        self.df = pd.concat([normal, medium, high])
        labels = [0]*500 + [1]*300 + [2]*200
        self.df['risk_level'] = labels
        
        X = self.df.drop('risk_level', axis=1)
        y = self.df['risk_level']
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
    
    def predict(self, hour, ip_risk, device_trust, geo_distance,
                fail_count, unusual_time, new_location, session_count):
        input_data = [[hour, ip_risk, device_trust, geo_distance,
                      fail_count, unusual_time, new_location, session_count]]
        risk_level = self.model.predict(input_data)[0]
        return int(risk_level)

print("✅ Модель создана")
