# Playing Card Classifier 🎴

A complete machine learning project that classifies playing cards using deep learning, featuring model training in PyTorch, a FastAPI backend, and a modern React frontend.

## 🎯 Project Overview

This project demonstrates an end-to-end machine learning pipeline for computer vision, specifically designed to classify all 53 types of playing cards (52 standard cards + joker). The system achieves **94.3% accuracy** on test data using a fine-tuned EfficientNet-B0 model.

### Key Features

- **Deep Learning Model**: Fine-tuned EfficientNet-B0 architecture with PyTorch
- **High Accuracy**: 94.3% test accuracy across 53 card classes
- **Production API**: FastAPI backend with CORS support
- **Modern Frontend**: React/Next.js application with real-time predictions
- **Complete Pipeline**: From data preprocessing to deployment

## 📊 Model Training & Data Science

### Dataset

The model is trained on the [Cards Image Dataset](https://www.kaggle.com/datasets/gpiosenka/cards-image-datasetclassification) containing:

- **7,624 training images** across 53 classes
- **Image size**: 224x224 pixels, resized to 128x128 for training

### Model Architecture

- **Base Model**: EfficientNet-B0 (pre-trained on ImageNet)
- **Transfer Learning**: Frozen feature extractor + custom classifier
- **Architecture**:
  ```python
  class SimpleCardClassifier(nn.Module):
      def __init__(self, num_classes=53):
          super().__init__()
          self.base_model = timm.create_model('efficientnet_b0', pretrained=True)
          self.features = nn.Sequential(*list(self.base_model.children())[:-1])
          self.classifier = nn.Sequential(
              nn.Flatten(),
              nn.Linear(self.base_model.num_features, num_classes)
          )
  ```

### Training Configuration

- **Optimiser**: Adam with learning rate scheduling
- **Loss Function**: CrossEntropyLoss
- **Batch Size**: 32
- **Epochs**: 5
- **Input Size**: 128x128 pixels
- **Data Augmentation**: Resize and normalisation transforms

### Training Results

The model training process is documented in `notebooks/playing_cards.ipynb` with the following progression:

| Epoch | Training Loss | Validation Loss |
| ----- | ------------- | --------------- |
| 1/5   | 1.565         | 0.512           |
| 2/5   | 0.544         | 0.284           |
| 3/5   | 0.338         | 0.203           |
| 4/5   | 0.228         | 0.217           |
| 5/5   | 0.179         | 0.182           |

**Final Test Accuracy: 94.34%**

## 🚀 API Deployment

### FastAPI Backend (`/api`)

The trained model is deployed using FastAPI with the following features:

- **Endpoint**: `POST /predict/` - Upload image file for classification
- **Model Loading**: Automatic PyTorch model loading on startup
- **Image Processing**: PIL-based image preprocessing pipeline
- **Response Format**: JSON with prediction and confidence score
- **CORS Support**: Configured for frontend integration

#### API Usage

```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@card_image.jpg"
```

#### Response Format

```json
{
  "filename": "card_image.jpg",
  "prediction": "ace of spades",
  "probability": 0.9876
}
```

### Model Specifications

- **Model File**: `pytorch_playing_cards_model-0.1.0.pth`
- **Classes**: 53 card types (ace through king for all suits + joker)
- **Input Processing**: 128x128 RGB images
- **Inference Time**: ~25ms per prediction

## 🖥️ Frontend Application

### React/Next.js Interface (`/app`)

A modern, responsive web application built with:

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS for responsive design
- **Features**:
  - Real-time image preview
  - Instant prediction results
  - Confidence score display
  - Mobile-responsive design

### Key Features

- **Image Upload**: Support for all common image formats
- **Live Preview**: Immediate visual feedback
- **Prediction Display**: Clear card name and confidence percentage
- **Error Handling**: Graceful error messages and validation
- **Performance**: Optimised bundle size and fast loading

## 📁 Project Structure

```
playing-card-classifier/
├── notebooks/
│   ├── playing_cards.ipynb          # Complete model training notebook
│   ├── data/                        # Kaggle dataset
│   └── models/                      # Saved model files
├── api/
│   ├── main.py                      # FastAPI application
│   ├── model/
│   │   ├── model.py                 # Model loading and inference
│   │   └── pytorch_playing_cards_model-0.1.0.pth
│   └── requirements.txt             # Python dependencies
├── app/
│   ├── src/app/
│   │   ├── page.tsx                 # Main React component
│   │   └── layout.tsx               # App layout
│   ├── package.json                 # Node.js dependencies
│   └── tailwind.config.ts           # Tailwind configuration
├── images/                          # Example predictions
└── dockerfile                       # Container deployment
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PyTorch 2.2+

### 1. Clone the Repository

```bash
git clone https://github.com/kevinwchen/playing-card-classifier
cd playing-card-classifier
```

### 2. Set Up the API

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Set Up the Frontend

```bash
cd app
npm install
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

## 📈 Example Predictions

The model demonstrates excellent performance across different card types (note that the images used for training have been cropped to only include the playing card):

### Six of Diamonds

**Prediction**: six of diamonds  
**Confidence**: 99.2%

![Six of Diamonds Prediction](images/6-of-diamonds-predict.png)

### King of Hearts

**Prediction**: king of hearts  
**Confidence**: 97.7%

![King of Hearts Prediction](images/king-of-hearts-predict.png)

## 🔬 Technical Details

### Model Performance

- **Test Accuracy**: 94.3%
- **Model Size**: 20.7 MB
- **Inference Speed**: ~50ms per image

### Technology Stack

- **ML Framework**: PyTorch, timm (EfficientNet)
- **Backend**: FastAPI, Uvicorn
- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **Data Processing**: PIL, NumPy, pandas
- **Development**: Jupyter notebooks, Git

### Deployment Options

- **Local Development**: Separate API and frontend servers
- **Docker**: Containerised deployment with included Dockerfile
- **Production**: API deployed on cloud platforms, frontend on Vercel

## 📚 Key Learnings

This project demonstrates several important machine learning concepts:

1. **Transfer Learning**: Leveraging pre-trained EfficientNet for faster training
2. **Data Pipeline**: Proper train/validation/test splits and data loading
3. **Model Deployment**: Converting research code to production API
4. **Full-Stack Integration**: Connecting ML models to web applications
