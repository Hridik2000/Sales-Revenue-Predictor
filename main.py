from fastapi import FastAPI
from Schema import RevenueRequest
from predict import predict_revenue

app = FastAPI(
    title="Sales Revenue Prediction API",
    version="1.0"
)

@app.get("/")
def home():
    return {"message": "Revenue Prediction API Running"}

@app.post("/predict")
def predict(data: RevenueRequest):

    revenue = predict_revenue(data)

    return {
        "predicted_revenue": round(revenue, 2)
    }