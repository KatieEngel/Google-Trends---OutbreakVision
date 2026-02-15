# OutbreakVision: Predictive Epidemiological Modeling

Traditional disease tracking is reactive, so our team aimed to forecast outbreaks before they peak. OutbreakVision is a predictive web application built during a rapid-prototyping hackathon that forecasts US influenza cases a full three weeks in advance.

## 1. Data Engineering & Signal Extraction
My specific role was to engineer the data pipeline to predict viral spread.
* **Data Sourcing:** Collected five years of ground-truth case data from the WHO and correlated it with historical Google Trends search frequencies.
* **Feature Engineering:** Identified and extracted high-signal consumer search queries (e.g., "how to stop a cough," "body aches no fever," "sore throat") to serve as leading indicators.

## 2. Machine Learning & Predictive Modeling
Developed and evaluated multiple machine learning models to determine the most accurate approach for time-series epidemiological forecasting.
* **Model Evaluation:** Trained and compared XGBoost, Random Forest, and Linear Regression models against the dataset.
* **Optimization:** Identified Linear Regression as the most performant model for this specific dataset. Iteratively tuned its hyperparameters to maximize predictive accuracy for the three-week forecasting window.

## 3. Web Deployment & Cross-Functional Teamwork
Built during a rapid-prototyping hackathon environment, the project required strong communication and agile development.
* **Visualization:** Integrated the optimized ML model into a web application, creating a dynamic dashboard that visualized five years of historical WHO data overlaid with our model's real-time predictive trendlines.
* **Collaboration:** Navigated the challenges of a fast-paced team environment, learning how to adapt, troubleshoot miscommunications, and leverage each team member's unique strengths to deliver a successful full-stack product.

## Tech Stack
* **Languages:** Python, HTML/CSS/JS
* **Machine Learning:** Scikit-learn, XGBoost, Random Forest, Linear Regression
* **Data & APIs:** Google Trends API, WHO Datasets, Pandas
