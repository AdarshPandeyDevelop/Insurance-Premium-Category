from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# Want to use it then Use this link -> http://127.0.0.1:8000/docs because it doesn't have GET HTTP Method, and only have POST HTTP Method, so use http://127.0.0.1:8000/docs

# import the ml model

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi",
                 "Bangalore", "Chennai", "Hyderabad", "Pune"]

tier_2_cities = ["Jaipur", "chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram",
                 "Ludhiana", "Nashik", "Prayagraj", "Udaipur", "SambhajiNagar", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirapalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "kozhikode", "Warangal", "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"]

# pydantic model to validate incoming data


class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120,
                              description="Age of the user")]
    weight: Annotated[float,
                      Field(..., gt=0, description="Weight of the user")]
    height: Annotated[float,
                      Field(..., gt=0, lt=2.5, description="Height of the user")]
    income_lpa: Annotated[float,
                          Field(..., gt=0,  description="Annual Salary of the user")]
    smoker: Annotated[bool, Field(..., description="Is user a smoker")]
    city: Annotated[str, Field(..., description="The city user belongs to")]
    occupation: Annotated[Literal['Engineer', 'Business', 'Doctor', 'Farmer', 'Driver', 'Teacher',
                                  'Private Job', 'Student', 'Government Job', 'Freelancer'], Field(..., description="Occupation of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "medium"

    @computed_field
    @property
    def age_group(self) -> str:  # add -> str here
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


@app.get("/")
def home():
    return {"message": "Hello world"}


@app.post("/predict")
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})
