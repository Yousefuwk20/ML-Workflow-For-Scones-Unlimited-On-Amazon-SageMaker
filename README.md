# ML Workflow For Scones Unlimited On Amazon SageMaker

> An end-to-end machine learning workflow on AWS for image classification using SageMaker, Lambda, and Step Functions

![AWS](https://img.shields.io/badge/AWS-SageMaker-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)

[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?logo=aws-lambda&logoColor=white)](https://aws.amazon.com/lambda/)
[![Step Functions](https://img.shields.io/badge/AWS-Step_Functions-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/step-functions/)
[![SageMaker](https://img.shields.io/badge/AWS-SageMaker-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/sagemaker/)


## 🎯 Overview

This project implements an event-driven machine learning workflow for **Scones Unlimited**, a scone-delivery-focused logistics company. The system uses AWS services to classify images of bicycles and motorcycles, helping to route delivery drivers more efficiently.

The workflow demonstrates:
- **Data extraction** from CIFAR-100 dataset
- **Model training** using SageMaker's built-in Image Classification algorithm
- **Serverless inference** using Lambda and Step Functions
- **Model monitoring** with SageMaker Model Monitor

**Project Context:** Final project for AWS AI/ML Scholarship Program

## 🏗️ Project Architecture

```
┌─────────────┐
│   S3 Bucket │ (Training Data & Model Storage)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ SageMaker       │ (Model Training & Deployment)
│ Training Job    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ SageMaker       │
│ Endpoint        │
└──────┬──────────┘
       │
       ▼
┌──────────────────────────────────────┐
│     AWS Step Functions Workflow      │
│                                      │
│  ┌───────────┐   ┌──────────┐        │
│  │ Serialize │──▶│ Classify │──┐    |
│  │  (Lambda) │   │ (Lambda) │   │    │
│  └───────────┘   └──────────┘   │    │
│                                 ▼    │
│                       ┌──────────┐   │
│                       │  Filter  │   │
│                       │ (Lambda) │   │
│                       └──────────┘   │
└──────────────────────────────────────┘
       │
       ▼
┌─────────────────┐
│ Model Monitor   │ (Data Capture & Monitoring)
└─────────────────┘
```

## ✨ Features

- **Automated ETL Pipeline**: Extract, transform, and load CIFAR-100 dataset
- **Image Classification**: Binary classification (bicycle vs. motorcycle)
- **Serverless Architecture**: Event-driven workflow using AWS Lambda and Step Functions
- **Model Monitoring**: Real-time inference tracking with SageMaker Model Monitor
- **Confidence Threshold Filtering**: Only pass high-confidence predictions to downstream systems
- **Scalable Deployment**: Production-ready ML infrastructure on AWS

## 📁 Project Structure

```
ML-Workflow-For-Scones-Unlimited-On-Amazon-SageMaker/
├── README.md                          # Project documentation
├── starter.ipynb                      # Main Jupyter notebook
├── step_function.json                 # Step Functions state machine definition
├── lambda functions/                  # Lambda function code
│   ├── serialize.py                   # Image serialization function
│   ├── Classify.py                    # Image classification function
│   └── filter.py                      # Confidence threshold filter
├── captured_data/                     # Model Monitor data
│   └── data.jsonl                     # Captured inference data
└── screencaps/                        # Screenshots and visualizations
    └── t.txt
```

## 🔄 Workflow Details

### Step 1: Serialize Image Data
**Lambda Function:** `serialize.py`
- Retrieves image from S3 bucket
- Encodes image as base64 string
- Passes data to next step

**Input:**
```json
{
  "s3_bucket": "bucket-name",
  "s3_key": "test/bicycle_s_000513.png",
  "image_data": ""
}
```

**Output:**
```json
{
  "statusCode": 200,
  "body": {
    "image_data": "base64_encoded_image",
    "s3_bucket": "bucket-name",
    "s3_key": "test/bicycle_s_000513.png",
    "inferences": []
  }
}
```

### Step 2: Classify Image
**Lambda Function:** `Classify.py`
- Decodes base64 image
- Invokes SageMaker endpoint
- Returns prediction probabilities

**Output:**
```json
{
  "statusCode": 200,
  "body": {
    "image_data": "...",
    "s3_bucket": "...",
    "s3_key": "...",
    "inferences": [0.95, 0.05]  // [bicycle_prob, motorcycle_prob]
  }
}
```

### Step 3: Filter Low Confidence
**Lambda Function:** `filter.py`
- Checks if max confidence exceeds threshold (0.88)
- Passes high-confidence predictions
- Raises exception for low-confidence predictions

## 🧩 Lambda Functions

### 1. serializeImageData
Downloads images from S3 and prepares them for inference.

### 2. classifyImage
Performs image classification using the SageMaker endpoint.

### 3. filterInferences
Filters predictions based on confidence threshold.

## 🎓 Model Training

### Training Configuration
```python
instance_type = 'ml.p2.xlarge'
hyperparameters = {
    'image_shape': '3,32,32',
    'num_classes': 2,
    'num_training_samples': 1000
}
```

### Model Performance
- **Validation Accuracy:** ~80%+
- **Instance Type:** ml.p2.xlarge (GPU instance)
- **Algorithm:** SageMaker Image Classification (ResNet-based)

## 📊 Monitoring

### SageMaker Model Monitor

**Captured Data:**
- Input images (base64 encoded)
- Model predictions
- Inference timestamps
- Confidence scores

### Visualization
The notebook includes visualization code to:
- Plot inference confidence over time
- Display captured images with predictions
- Identify predictions below threshold
- Monitor model performance trends

## 📈 Results

### Key Achievements
Successfully deployed end-to-end ML workflow on AWS  
Achieved 80%+ validation accuracy on bicycle/motorcycle classification  
Implemented serverless architecture for scalable inference  
Configured real-time model monitoring  
Established confidence-based filtering system  

### Sample Inference Results
- Bicycle images: 91-95% confidence (passed)
- Motorcycle images: 85-92% confidence (passed)
- Ambiguous images: <88% confidence (filtered out)
