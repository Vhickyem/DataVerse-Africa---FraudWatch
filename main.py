from typing import Literal
from datetime import datetime, date
import pandas as pd
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from feature_interactions import FeatureInteractions
from drop_columns import DropColumns


# Load pipeline
pipeline = joblib.load("fraud_detection_model.pkl")

# FastAPI app
app = FastAPI(title="Fraud Detection API")

# Request schema
class InputData(BaseModel):
    transaction_id: str
    user_id: str
    transaction_type: Literal['Withdraw Cash', 'Send Money', 'Deposit Cash', 'Lipa na M-Pesa', 'Buy Airtime', 'Pay Bill']
    amount: float
    location: Literal['Nakuru', 'Garissa', 'Nyeri', 'Nairobi', 'Machakos', 'Meru', 'Kisumu', 'Mombasa', 'Eldoret', 'Thika']
    device_type: Literal["Feature Phone", "Ios", "Android"]
    network_provider: Literal['Telkom Kenya', 'Safaricom', 'Airtel']
    user_type: Literal["Individual", "Agent"]
    time_of_day: Literal["Morning", "Afternoon", "Evening", "Night"]
    is_foreign_number: int
    is_sim_recently_swapped: int
    has_multiple_accounts: int
    datetime: datetime
    date: date
    hour: int


@app.post("/predict")
def predict(input_data: InputData = Body(...)):
    try:
        # Convert to DataFrame-like structure
        # Use model_dump to convert Pydantic model to dict
        input_dict = input_data.model_dump()
        X = pd.DataFrame([input_dict])
        # predict
        prediction = pipeline.predict(X)
        return {"prediction": "Non-Fraudulent" if int(prediction[0]) == 1 else "Fraudulent"}
    except Exception as e:
        import traceback
        traceback.print_exc()  # print the full error in terminal
        raise HTTPException(status_code=500, detail=str(e))
