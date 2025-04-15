# CT Scan Analysis Website - Deployment Guide

## Overview

This document provides instructions for deploying the CT Scan Analysis Website for sinusitis detection. The website allows ENT specialists to upload CT images or videos for automated analysis using multiple classification systems.

## Features

- **Lund-Mackay Scoring System**: Evaluates the degree of sinus opacification
- **Haller Cells Detection**: Identifies infraorbital ethmoidal air cells
- **Kuros Classification**: Grades sinusitis severity
- **Skull Base Defect Detection**: Identifies potential skull base defects
- **Admin Feedback System**: Allows authorized users to provide feedback to improve algorithm accuracy

## Deployment Options

### Option 1: Local Deployment

1. Ensure Python 3.8+ is installed
2. Install required dependencies:
   ```
   pip install flask opencv-python numpy
   ```
3. Navigate to the project directory
4. Run the application:
   ```
   python app.py
   ```
5. Access the website at http://localhost:5000

### Option 2: Production Deployment

For production deployment, we recommend using Docker and a web server like Nginx.

1. Build the Docker image:
   ```
   docker build -t ct-scan-analysis .
   ```
2. Run the container:
   ```
   docker run -d -p 8000:5000 ct-scan-analysis
   ```
3. Configure Nginx as a reverse proxy (sample configuration provided in `nginx.conf`)
4. Set up HTTPS with Let's Encrypt or similar service

## Admin Access

The website includes an admin section for authorized users to provide feedback and improve the algorithm.

- Admin URL: `/admin`
- Default credentials:
  - Username: `admin`
  - Password: `ct_admin_2025`

**Important**: Change these credentials before deploying to production.

## Directory Structure

```
ct_scan_project/
├── app.py                  # Main Flask application
├── models/                 # Machine learning models
│   ├── lund_mackay.py      # Lund-Mackay scoring implementation
│   ├── kuros.py            # Kuros classification implementation
│   ├── skull_base.py       # Skull base defect detection implementation
│   ├── haller_detector.py  # Haller cell detection implementation
│   └── feedback.py         # Feedback management system
├── static/                 # Static files
│   ├── js/                 # JavaScript files
│   ├── css/                # CSS files
│   └── images/             # Image assets
├── templates/              # HTML templates
│   ├── index.html          # Main page
│   └── admin.html          # Admin interface
├── uploads/                # Directory for uploaded files
├── data/                   # Data storage
│   └── feedback/           # Feedback and analysis storage
└── utils/                  # Utility functions
    └── preprocessing.py    # Image preprocessing functions
```

## Configuration

Configuration settings are defined in the `Config` class within `app.py`. Key settings include:

- `SECRET_KEY`: Used for session security (change for production)
- `UPLOAD_FOLDER`: Directory for uploaded files
- `ALLOWED_EXTENSIONS`: Allowed file types for upload
- `ADMIN_USERNAME` and `ADMIN_PASSWORD`: Admin credentials

## Maintenance

- Regularly backup the `data/feedback` directory to preserve learning data
- Monitor disk usage in the `uploads` directory and implement cleanup as needed
- Update dependencies regularly for security patches

## Troubleshooting

- If the application fails to start, check Python version and installed dependencies
- If uploads fail, verify the `uploads` directory has proper permissions
- For image processing errors, ensure OpenCV is properly installed
