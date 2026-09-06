Heart Disease Prediction – IITM BS MLOps OPPE-2 (May 2026)

Project Overview

This project implements a production-oriented Heart Disease Prediction System as part of the IIT Madras BS MLOps OPPE-2 (May 2026).

The solution covers the complete MLOps lifecycle:

Machine learning model training

Explainability using SHAP

Fairness evaluation using Fairlearn

REST API using FastAPI

Docker containerization

Deployment on Google Kubernetes Engine (GKE)

Horizontal Pod Autoscaling (HPA)

GitHub Actions CI/CD

Prediction logging

Load testing using wrk

Input data drift detection using PSI

Dataset

The project uses the heart disease dataset available in:

data/data.csv

The dataset contains 303 records and 14 clinical input attributes plus the target.

Model Inputs

age

gender

cp

trestbps

chol

fbs

restecg

thalach

exang

oldpeak

slope

ca

thal

The sno column is treated as an identifier and is not used for model training.

The target is converted from:

yes / no

to:

1 / 0

Missing numerical values are handled using median imputation and categorical values using most-frequent imputation.

Machine Learning Model

A scikit-learn pipeline is used with:

Numerical preprocessing

Median imputation

StandardScaler

Categorical preprocessing

Most-frequent imputation

OneHotEncoder

Classification model

Logistic Regression

The trained model is saved as:

heart_disease_model.joblib

Explainability – SHAP

SHAP (SHapley Additive exPlanations) is used to understand feature importance.

The most influential features observed in the analysis include:

Chest pain type (cp)

Thalassemia (thal)

ST depression (oldpeak)

Exercise-induced angina (exang)

Number of major vessels (ca)

Lower-impact features in the analysis included age, fasting blood sugar, resting ECG and resting blood pressure.

SHAP magnitude represents the importance of a feature. It does not by itself indicate whether the feature increases or decreases the predicted risk.

Fairness – Fairlearn

Fairness testing is performed using age as the sensitive attribute, as required by the problem statement.

The following metrics were evaluated:

Accuracy

Precision

Recall

Selection rate

Demographic Parity Difference

Equalized Odds Difference

Observed results:

Demographic Parity Difference: 1.0
Equalized Odds Difference:     1.0

These values indicate substantial measured disparity across age groups. However, several age groups contain very few samples, so the group-level estimates can be unstable and should be interpreted as a fairness warning rather than proof that age alone causes prediction differences.

API

The prediction service is implemented using FastAPI.

Endpoints

Health Check

GET /health

Returns the API health status and timestamp.

Prediction

POST /predict

Accepts patient information and returns:

Prediction

Prediction label

Probability

Timestamp

Example request:

{
  "age": 55,
  "gender": "male",
  "cp": 1,
  "trestbps": 140,
  "chol": 250,
  "fbs": 0,
  "restecg": 1,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 1.0,
  "slope": 1,
  "ca": 0,
  "thal": 2
}

Docker

The API is containerized using Docker.

Build:

docker build -t heart-disease-api:1.0 .

Run locally:

docker run -d --name heart-disease-api-container -p 8000:8000 heart-disease-api:1.0

The Docker image is stored in Google Artifact Registry.

Google Cloud Deployment

Artifact Registry

The Docker image is stored in:

us-central1-docker.pkg.dev/project-6a8fefef-8f20-4069-96f/mlops-repo/heart-disease-api

Google Kubernetes Engine

The application is deployed to:

Cluster: heart-disease-cluster
Region: us-east1

Kubernetes resources:

deployment.yaml
service.yaml
hpa.yaml

The service uses a Kubernetes LoadBalancer to expose the API externally.

Autoscaling

Horizontal Pod Autoscaling is configured using CPU utilization.

Configuration:

Minimum replicas: 1
Maximum replicas: 3
CPU target: 70%

This allows Kubernetes to automatically increase the number of API pods when traffic increases.

CI/CD

GitHub Actions is used to automate the container build and deployment workflow.

Workflow file:

.github/workflows/deploy.yml

The workflow:

Checks out the repository

Authenticates to Google Cloud using GitHub OIDC / Workload Identity Federation

Configures Docker authentication

Builds the Docker image

Pushes the image to Artifact Registry

Workload Identity Federation is used instead of storing a long-lived Google Cloud service-account JSON key.

Prediction Logging

The API logs each prediction request individually.

Each log entry contains:

Event type

Input features

Prediction

Prediction probability

Timestamp

Example:

{
  "event": "prediction",
  "inputs": {},
  "prediction": 1,
  "probability": 0.6762,
  "timestamp": "2026-09-06T00:00:00+00:00"
}

A 100-row random prediction dataset was generated:

prediction_data_100.csv

All 100 samples were sent individually to the deployed API.

Result:

Successful predictions: 100 / 100

Load Testing

Load testing was performed using wrk with more than 2,000 concurrent connections.

Command:

wrk -t4 -c2000 -d30s http://35.237.198.195/health

Observed results:

Concurrent connections: 2000
Threads:                4
Test duration:          30 seconds
Requests/sec:           911.67
Average latency:        886.85 ms
Maximum latency:        2.00 s
Timeouts:                8270
Read errors:             1
Requests:               27387

Load Test Analysis

The API sustained approximately 912 requests/second under 2,000 concurrent connections. However, the high number of timeouts indicates that the deployment reached its capacity under this load and that additional optimization or scaling would be required for sustained high-concurrency production traffic.

Input Drift Detection

Input drift was evaluated by comparing the training dataset with the generated 100-row prediction dataset using the Population Stability Index (PSI).

Observed PSI values:

Feature

PSI

age

0.7004

cp

0.8687

trestbps

0.8784

chol

1.5396

fbs

Not calculated

restecg

0.2335

thalach

0.3866

exang

Not calculated

oldpeak

1.2997

slope

0.2245

ca

1.0757

thal

0.8071

A PSI value above approximately 0.25 is commonly treated as evidence of meaningful distribution shift.

The analysis therefore indicates substantial input drift, especially for:

cholesterol (chol)

oldpeak

ca

trestbps

cp

thal

age

Persistent drift should trigger investigation of the production data distribution and consideration of model retraining.

Project Structure

22F1001845_IITMBS_MLOPS_OPPE2_MAY_2026/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── data/
│   └── data.csv
│
├── HeartDiseaseTrainingAndPrediction.ipynb
├── app.py
├── Dockerfile
├── deployment.yaml
├── service.yaml
├── hpa.yaml
├── requirements.txt
├── heart_disease_model.joblib
├── prediction_data_100.csv
└── README.md

Key Technologies

Python

Pandas

NumPy

Scikit-learn

SHAP

Fairlearn

FastAPI

Uvicorn

Docker

Google Artifact Registry

Google Kubernetes Engine

Kubernetes

Horizontal Pod Autoscaler

GitHub Actions

Workload Identity Federation

Google Cloud Logging

wrk

Conclusion

This project demonstrates an end-to-end MLOps workflow for a heart disease prediction application, including model development, explainability, fairness analysis, containerization, cloud deployment, autoscaling, CI/CD, observability, performance testing and data drift monitoring.
