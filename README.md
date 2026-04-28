Here's a clean, GitHub-ready project description for you:

---

## 🏠 House Haven — Bengaluru Real Estate Price Predictor

**House Haven** is an end-to-end machine learning web application that predicts residential property prices across Bengaluru using a trained Random Forest model. The project covers the full data science pipeline — from raw data ingestion and exploratory analysis to model deployment via an elegant, premium-styled Streamlit interface.

### 📊 Data & EDA
The project uses the **Bengaluru House Data** dataset. During preprocessing, irrelevant columns (`area_type`, `balcony`, `society`, `availability`) were dropped, missing values were imputed using median/mode strategies, and duplicate records were removed. The `size` column was parsed to extract BHK counts, and `total_sqft` was cleaned to handle range values. Locations with fewer than 10 listings were consolidated into an `others` category to reduce noise. A `price_per_sqft` feature was engineered to facilitate outlier detection via IQR-based filtering, and BHK/bathroom combinations were validated for realism. Finally, location was one-hot encoded for model compatibility.

### 🤖 Model
A **Random Forest Regressor** was trained with hyperparameter tuning via `GridSearchCV` (tuning `n_estimators` and `max_depth` across a 5-fold cross-validation). The best model and feature columns are exported using `joblib` for deployment.

### 🖥️ Streamlit App
The deployed app (`app.py`) allows users to select a **location**, **square footage**, **BHK**, and **bathroom count**, then instantly generates a market valuation. Results are displayed in INR (Lakhs/Crores) alongside **comparative market analytics** — including a regional price distribution histogram, price-per-sqft benchmarking, and segment min/median/max metrics.

### 🛠️ Tech Stack
`Python` · `Pandas` · `Scikit-learn` · `Streamlit` · `Matplotlib` · `Seaborn` · `Joblib`

---

Feel free to ask if you'd like a shorter version, a `README.md` file, or badges added!
