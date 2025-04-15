# CT Scan Analysis Website - Implementation Plan

## 1. Environment Setup

First, let's set up our development environment with the necessary libraries for image processing and web development.

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install required packages
pip install flask opencv-python numpy scikit-image pillow tensorflow matplotlib dicom2nifti pydicom flask-cors

# Frontend dependencies
npm init -y
npm install react react-dom react-scripts bootstrap axios three
```

## 2. Project Structure

```
ct_scan_project/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models/                 # Machine learning models
│   ├── __init__.py
│   ├── lund_mackay.py      # Lund-Mackay scoring implementation
│   ├── kuros.py            # Kuros classification implementation
│   ├── harshala.py         # Harshala classification implementation
│   ├── haller_detector.py  # Haller cell detection implementation
├── static/                 # Static files
│   ├── js/                 # JavaScript files
│   ├── css/                # CSS files
│   ├── images/             # Image assets
├── templates/              # HTML templates
│   ├── index.html          # Main page
│   ├── results.html        # Results page
├── uploads/                # Directory for uploaded files
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── preprocessing.py    # Image preprocessing functions
│   ├── visualization.py    # Visualization functions
├── requirements.txt        # Python dependencies
```

## 3. Backend Implementation

### 3.1 Flask Application Setup

```python
# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from models.lund_mackay import analyze_lund_mackay
from models.haller_detector import detect_haller_cells
# Import other models as they are implemented
from utils.preprocessing import preprocess_image
import config

app = Flask(__name__)
app.config.from_object(config.Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = str(uuid.uuid4()) + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the file asynchronously (in a real app)
        # For now, we'll process it synchronously
        result = process_file(filepath)
        
        return jsonify(result)
    
    return jsonify({'error': 'File type not allowed'}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_file(filepath):
    # Preprocess the image
    preprocessed_image = preprocess_image(filepath)
    
    # Analyze using different models
    lund_mackay_result = analyze_lund_mackay(preprocessed_image)
    haller_cells_result = detect_haller_cells(preprocessed_image)
    
    # TODO: Add other analyses as they are implemented
    
    # Combine results
    result = {
        'lund_mackay': lund_mackay_result,
        'haller_cells': haller_cells_result,
        # Add other results here
    }
    
    return result

@app.route('/results/<result_id>')
def get_results(result_id):
    # In a real app, this would fetch results from a database
    # For now, we'll just render a template
    return render_template('results.html', result_id=result_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 3.2 Configuration

```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-development'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'dcm', 'dicom', 'mp4', 'avi', 'mov'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
```

## 4. Image Processing Implementation

### 4.1 Preprocessing Utilities

```python
# utils/preprocessing.py
import cv2
import numpy as np
import pydicom
import os

def preprocess_image(filepath):
    """
    Preprocess the input image file based on its type
    """
    file_ext = os.path.splitext(filepath)[1].lower()
    
    if file_ext in ['.dcm', '.dicom']:
        return preprocess_dicom(filepath)
    elif file_ext in ['.png', '.jpg', '.jpeg', '.gif']:
        return preprocess_regular_image(filepath)
    elif file_ext in ['.mp4', '.avi', '.mov']:
        return preprocess_video(filepath)
    else:
        raise ValueError(f"Unsupported file extension: {file_ext}")

def preprocess_dicom(filepath):
    """
    Preprocess DICOM files
    """
    dicom_data = pydicom.dcmread(filepath)
    image = dicom_data.pixel_array
    
    # Normalize to 0-255 range
    image = image - np.min(image)
    if np.max(image) > 0:
        image = image / np.max(image) * 255
    
    image = image.astype(np.uint8)
    
    # Apply additional preprocessing as needed
    # e.g., contrast enhancement, noise reduction
    
    return image

def preprocess_regular_image(filepath):
    """
    Preprocess regular image files (PNG, JPG, etc.)
    """
    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    
    # Apply preprocessing as needed
    # e.g., resize, normalize, enhance contrast
    
    return image

def preprocess_video(filepath):
    """
    Extract frames from video and preprocess them
    """
    frames = []
    cap = cv2.VideoCapture(filepath)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply preprocessing as needed
        
        frames.append(gray_frame)
    
    cap.release()
    
    # For simplicity, we'll just return the middle frame for now
    # In a real implementation, you might want to process all frames
    if frames:
        return frames[len(frames) // 2]
    else:
        raise ValueError("No frames could be extracted from the video")
```

### 4.2 Lund-Mackay Scoring Implementation

```python
# models/lund_mackay.py
import numpy as np
import cv2

def analyze_lund_mackay(image):
    """
    Implement Lund-Mackay scoring system for CT scans
    
    This is a simplified placeholder implementation.
    In a real application, this would use more sophisticated
    image processing or machine learning techniques.
    """
    # Placeholder implementation
    # In a real system, this would use segmentation and classification
    
    # For demonstration purposes, we'll return random scores
    # In a real implementation, this would analyze the actual image
    
    # Define the sinuses to score
    sinuses = [
        "right_maxillary", "left_maxillary",
        "right_anterior_ethmoid", "left_anterior_ethmoid",
        "right_posterior_ethmoid", "left_posterior_ethmoid",
        "right_sphenoid", "left_sphenoid",
        "right_frontal", "left_frontal",
        "right_omc", "left_omc"
    ]
    
    # Generate scores (0, 1, or 2) for each sinus
    # 0: no abnormality, 1: partial opacification, 2: complete opacification
    # For OMC: 0: not obstructed, 2: obstructed
    scores = {}
    total_score = 0
    
    for sinus in sinuses:
        if "omc" in sinus:
            # OMC is scored 0 or 2
            score = np.random.choice([0, 2])
        else:
            # Other sinuses are scored 0, 1, or 2
            score = np.random.randint(0, 3)
        
        scores[sinus] = score
        total_score += score
    
    return {
        "scores": scores,
        "total_score": total_score,
        "max_possible": 24,
        "interpretation": interpret_lund_mackay_score(total_score)
    }

def interpret_lund_mackay_score(score):
    """
    Interpret the Lund-Mackay score
    """
    if score <= 4:
        return "Normal or minimal disease"
    elif score <= 8:
        return "Mild disease"
    elif score <= 16:
        return "Moderate disease"
    else:
        return "Severe disease"
```

### 4.3 Haller Cell Detection Implementation

```python
# models/haller_detector.py
import numpy as np
import cv2

def detect_haller_cells(image):
    """
    Detect Haller cells (infraorbital ethmoidal air cells) in CT scans
    
    This is a simplified placeholder implementation.
    In a real application, this would use more sophisticated
    image processing or machine learning techniques.
    """
    # Placeholder implementation
    # In a real system, this would use segmentation and feature detection
    
    # For demonstration purposes, we'll return random results
    # In a real implementation, this would analyze the actual image
    
    detected = np.random.choice([True, False], p=[0.2, 0.8])  # 20% chance of detection
    
    if detected:
        # If detected, generate random location and size
        location = {
            "x": np.random.randint(100, 400),
            "y": np.random.randint(100, 400)
        }
        size = np.random.randint(5, 20)
        
        return {
            "detected": True,
            "location": location,
            "size": size,
            "clinical_significance": assess_clinical_significance(size)
        }
    else:
        return {
            "detected": False
        }

def assess_clinical_significance(size):
    """
    Assess the clinical significance of Haller cells based on size
    """
    if size < 10:
        return "Likely not clinically significant"
    else:
        return "May narrow the ipsilateral ostiomeatal complex, potentially predisposing to obstruction"
```

## 5. Frontend Implementation

### 5.1 Main HTML Template

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CT Scan Analysis for Sinusitis</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-12 text-center mb-4">
                <h1>CT Scan Analysis for Sinusitis</h1>
                <p class="lead">Upload CT images or videos for automated analysis</p>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Upload CT Scan</h5>
                        <form id="upload-form" enctype="multipart/form-data">
                            <div class="form-group">
                                <label for="file-upload">Select file</label>
                                <input type="file" class="form-control-file" id="file-upload" name="file" accept=".png,.jpg,.jpeg,.gif,.dcm,.dicom,.mp4,.avi,.mov">
                                <small class="form-text text-muted">Supported formats: PNG, JPG, DICOM, MP4, AVI, MOV</small>
                            </div>
                            <button type="submit" class="btn btn-primary btn-block">Analyze</button>
                        </form>
                    </div>
                </div>
                
                <div id="loading" class="text-center mt-4 d-none">
                    <div class="spinner-border text-primary" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                    <p>Processing your CT scan. This may take a moment...</p>
                </div>
                
                <div id="error-message" class="alert alert-danger mt-4 d-none"></div>
            </div>
        </div>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

### 5.2 JavaScript for File Upload

```javascript
// static/js/main.js
$(document).ready(function() {
    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        
        const fileInput = $('#file-upload')[0];
        if (fileInput.files.length === 0) {
            showError('Please select a file to upload');
            return;
        }
        
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        // Show loading indicator
        $('#loading').removeClass('d-none');
        $('#error-message').addClass('d-none');
        
        // Send file to server
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Hide loading indicator
                $('#loading').addClass('d-none');
                
                // Redirect to results page or display results
                displayResults(response);
            },
            error: function(xhr) {
                // Hide loading indicator
                $('#loading').addClass('d-none');
                
                // Show error message
                let errorMessage = 'An error occurred during file upload';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                showError(errorMessage);
            }
        });
    });
    
    function showError(message) {
        const errorElement = $('#error-message');
        errorElement.text(message);
        errorElement.removeClass('d-none');
    }
    
    function displayResults(results) {
        // For now, we'll redirect to a new page with the results
        // In a more advanced implementation, this could display results directly
        
        // Create a results container
        const resultsHtml = `
            <div class="card mt-4">
                <div class="card-header">
                    <h5>Analysis Results</h5>
                </div>
                <div class="card-body">
                    <h6>Lund-Mackay Score</h6>
                    <p>Total Score: ${results.lund_mackay.total_score} / ${results.lund_mackay.max_possible}</p>
                    <p>Interpretation: ${results.lund_mackay.interpretation}</p>
                    
                    <h6>Haller Cells</h6>
                    <p>${results.haller_cells.detected ? 
                        `Detected: Yes<br>Clinical Significance: ${results.haller_cells.clinical_significance}` : 
                        'Detected: No'}</p>
                    
                    <!-- Add other results here as they are implemented -->
                </div>
            </div>
        `;
        
        // Append results to the page
        $('#upload-form').after(resultsHtml);
        $('#upload-form')[0].reset();
    }
});
```

### 5.3 CSS Styling

```css
/* static/css/style.css */
body {
    background-color: #f8f9fa;
}

.container {
    max-width: 800px;
}

.card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

#loading {
    padding: 20px;
}

#error-message {
    margin-top: 20px;
}
```

## 6. Next Steps

1. Implement the remaining classification systems (Kuros and Harshala)
2. Develop more sophisticated image processing algorithms
3. Implement visualization of CT scans with highlighted features
4. Add user authentication if required
5. Set up database for storing results
6. Implement comprehensive testing
7. Prepare for deployment
