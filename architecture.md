# CT Scan Analysis Website Architecture

## Overview
This document outlines the architecture for a web application that analyzes CT scans for sinus disease and sinusitis. The application will allow ENT specialists to upload CT images or videos and will provide analysis based on multiple classification systems.

## System Components

### 1. Frontend
- **User Interface**: Responsive web interface built with HTML5, CSS3, and JavaScript
- **Framework**: React.js for component-based UI development
- **Features**:
  - File upload component for CT images and videos
  - Results dashboard displaying analysis outcomes
  - Visualization of CT scans with highlighted features
  - User authentication (optional)

### 2. Backend
- **Web Framework**: Flask (Python)
- **API Endpoints**:
  - `/upload` - For receiving CT scan files
  - `/analyze` - For processing uploaded files
  - `/results` - For retrieving analysis results

### 3. Image Processing Pipeline
- **Libraries**: OpenCV, PyDicom, scikit-image
- **Preprocessing**:
  - DICOM file parsing
  - Image normalization and enhancement
  - Segmentation of sinus regions

### 4. Analysis Modules
- **Lund-Mackay Scoring System**:
  - Detection of sinus opacification
  - Scoring based on opacification levels (0-2)
  - Calculation of total score (max 24)
  
- **Kuros Classification**:
  - Implementation based on further research
  
- **Harshala Classification**:
  - Implementation based on further research
  
- **Haller Cell Detection**:
  - Identification of infraorbital ethmoidal air cells
  - Assessment of their impact on ostiomeatal complex

### 5. Machine Learning Models
- **Model Architecture**: Convolutional Neural Networks (CNNs)
- **Training Data**: To be determined (may need synthetic data or public datasets)
- **Tasks**:
  - Segmentation of sinus regions
  - Classification of opacification levels
  - Detection of anatomical structures

### 6. Data Storage
- **File Storage**: Local file system for development, cloud storage for production
- **Database**: SQLite for development, PostgreSQL for production
- **Schema**:
  - Users table (if authentication is implemented)
  - Uploads table (metadata about uploaded files)
  - Results table (analysis outcomes)

### 7. Visualization Module
- **Libraries**: Three.js or D3.js
- **Features**:
  - 2D/3D rendering of CT scans
  - Highlighting of detected features
  - Color-coding based on classification results

## System Flow

1. User uploads CT scan images or video
2. System preprocesses the images
3. Analysis modules process the images:
   - Lund-Mackay scoring
   - Kuros classification
   - Harshala classification
   - Haller cell detection
4. Results are stored in the database
5. Visualization module renders the results
6. User views the analysis results on the dashboard

## Technical Requirements

### Development Environment
- Python 3.8+
- Node.js 14+
- Git for version control

### Deployment
- Docker for containerization
- Nginx as web server
- HTTPS for secure communication

### Performance Considerations
- Asynchronous processing for large files
- Caching of results for repeated analyses
- Optimization of machine learning models for inference speed

## Future Enhancements
- Integration with hospital PACS systems
- Batch processing of multiple CT scans
- Comparison of results over time for the same patient
- Export of results in medical report formats
