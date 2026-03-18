# Insurance-Premium-Category
Insurance Premium Category
# 🛡️ InsureIQ — Insurance Premium Category Predictor

A complete end-to-end Machine Learning project that predicts a user's **insurance premium category** (Low / Medium / High) based on personal, health, and lifestyle inputs.

Built with **Scikit-learn**, served via **FastAPI**, and visualized through a polished **Streamlit** UI.

---

## 📌 Table of Contents

- [Overview]
- [Project Structure]
- [How It Works]
- [Features]
- [Tech Stack]
- [Installation & Setup]
  - [Run Streamlit UI]
  - [Run FastAPI Backend]
- [API Usage]
- [Dataset]
- [Model Details]
- [Screenshots]
- [License]

---

## 📖 Overview

InsureIQ takes a user's demographic and lifestyle inputs and classifies them into one of three insurance premium brackets:

| Category | Meaning |
|----------|---------|
| 🟢 **Low** | Low-risk profile — affordable premiums likely |
| 🟡 **Medium** | Moderate risk — standard plans recommended |
| 🔴 **High** | Elevated risk — comprehensive coverage advised |

The project exposes two interfaces:
- A **FastAPI REST endpoint** (`/predict`) for programmatic access
- A **Streamlit web app** for interactive, browser-based predictions

---

## 📁 Project Structure

```
InsureIQ/
│
├── app.py                          # FastAPI backend with /predict endpoint
├── streamlit_app.py                # Streamlit frontend UI
├── ML_Model_used_in_FastAPI.ipynb  # Jupyter notebook — EDA, training, evaluation
├── model.pkl                       # Trained & serialized ML model (pickle)
├── insurance.csv                   # Raw dataset used for training
├── requirement.txt                 # Python dependencies
└── README.md                       # You're here!
```

---

## ⚙️ How It Works

### Input Fields

| Field | Type | Description |
|-------|------|-------------|
| `age` | int | Age of the user (1–119) |
| `weight` | float | Weight in kilograms |
| `height` | float | Height in meters |
| `income_lpa` | float | Annual income in Lakhs Per Annum (₹) |
| `smoker` | bool | Whether the user smokes |
| `city` | str | City of residence |
| `occupation` | str | One of 10 supported occupations |

### Derived Features (computed automatically)

These are calculated from the raw inputs and fed into the ML model:

| Feature | Formula / Logic |
|---------|----------------|
| `bmi` | `weight / height²` |
| `age_group` | young / adult / middle_aged / senior |
| `lifestyle_risk` | high / medium based on smoker + BMI |
| `city_tier` | 1 (metro) / 2 (tier-2) / 3 (other) |

---

## ✨ Features

- ✅ Real-time **BMI calculator** with color-coded category display
- ✅ Clean **Streamlit UI** with dark theme, live inputs, and styled result cards
- ✅ **FastAPI backend** with Pydantic validation and auto-generated Swagger docs
- ✅ Derived feature computation mirrors both frontend and backend — results are consistent
- ✅ City classification into **Tier 1 / 2 / 3** automatically
- ✅ Model trained on real-world-style insurance data with **10 occupations** and **50+ cities**

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| ML Model | Scikit-learn |
| Model Serialization | Pickle |
| Backend API | FastAPI + Uvicorn |
| Data Validation | Pydantic v2 |
| Frontend UI | Streamlit |
| Data Processing | Pandas, NumPy |
| Notebook | Jupyter |

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.9+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/InsureIQ.git
cd InsureIQ
```

### 2. Install Dependencies

```bash
pip install -r requirement.txt
```

> **Note:** If you face any version conflicts, create a virtual environment first:
> ```bash
> python -m venv venv
> source venv/bin/activate        # macOS/Linux
> venv\Scripts\activate           # Windows
> pip install -r requirement.txt
> ```

---

### Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

Then open your browser at: **http://localhost:8501**

---

### Run FastAPI Backend

```bash
uvicorn app:app --reload
```

Then open your browser at: **http://127.0.0.1:8000/docs**

> ⚠️ The app only has a `POST /predict` endpoint — use the `/docs` Swagger UI to test it, not the root URL directly.

---

## 🔌 API Usage

### Endpoint

```
POST /predict
```

### Request Body (JSON)

```json
{
  "age": 35,
  "weight": 75.5,
  "height": 1.75,
  "income_lpa": 12.5,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "Engineer"
}
```

### Response

```json
{
  "predicted_category": "low"
}
```

### Example with `curl`

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "weight": 90,
    "height": 1.70,
    "income_lpa": 8.0,
    "smoker": true,
    "city": "Delhi",
    "occupation": "Driver"
  }'
```

### Example with Python `requests`

```python
import requests

payload = {
    "age": 45,
    "weight": 90,
    "height": 1.70,
    "income_lpa": 8.0,
    "smoker": True,
    "city": "Delhi",
    "occupation": "Driver"
}

response = requests.post("http://127.0.0.1:8000/predict", json=payload)
print(response.json())
# Output: {'predicted_category': 'high'}
```

---

## 📊 Dataset

**File:** `insurance.csv`

| Column | Type | Description |
|--------|------|-------------|
| `age` | int | Age of the individual |
| `weight` | float | Body weight (kg) |
| `height` | float | Height (meters) |
| `income_lpa` | float | Annual income in LPA |
| `smoker` | str | yes / no |
| `city` | str | City of residence |
| `occupation` | str | Profession category |
| `insurance_premium_category` | str | **Target** — low / medium / high |

---

## 🤖 Model Details

The ML pipeline and feature engineering are documented in **`ML_Model_used_in_FastAPI.ipynb`**.

**Key steps in the notebook:**
1. Exploratory Data Analysis (EDA)
2. Feature Engineering — BMI, age group, lifestyle risk, city tier
3. Encoding categorical variables
4. Model training & hyperparameter tuning
5. Evaluation (accuracy, classification report)
6. Serialization to `model.pkl` via `pickle`

**Supported Occupations:**
`Engineer`, `Business`, `Doctor`, `Farmer`, `Driver`, `Teacher`, `Private Job`, `Student`, `Government Job`, `Freelancer`

**City Tiers:**
- **Tier 1:** Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Pune
- **Tier 2:** Jaipur, Lucknow, Bhopal, Nagpur, Indore, and 40+ more
- **Tier 3:** All other cities

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

> Built with ❤️ using Python, FastAPI, and Streamlit.
