# CT Scan Analysis Website - User Guide

## Overview

Welcome to the CT Scan Analysis Website for sinusitis detection. This application allows ENT specialists to upload CT images or videos for automated analysis using multiple classification systems.

## Features

### Main Analysis Features

- **Lund-Mackay Scoring System**: Evaluates the degree of sinus opacification in each sinus and provides a total score with interpretation
- **Haller Cells Detection**: Identifies infraorbital ethmoidal air cells and assesses their clinical significance
- **Kuros Classification**: Grades sinusitis severity from Grade 0 to Grade 3
- **Skull Base Defect Detection**: Identifies potential defects in the skull base that may require special attention during surgery
- **Surgery Difficulty Calculator**: Assesses the difficulty level of potential sinus surgery based on CT findings
- **Instrument Recommendations**: Suggests appropriate surgical instruments based on the calculated difficulty level
- **Visual Markers**: Highlights detected features on the CT scan image

### Admin Feedback System

The website includes a special admin section that allows you to provide feedback on analysis results. This feedback is used to improve the algorithm's accuracy over time.

## How to Use

### Analyzing CT Scans

1. Open the website in your browser
2. Click the "Choose File" button to select a CT scan image or video
3. Click the "Analyze" button to upload and process the file
4. View the analysis results, which include:
   - Lund-Mackay scores for each sinus and total score
   - Haller cells detection results
   - Kuros classification
   - Skull base defect detection
   - Surgery difficulty assessment with recommended instruments
   - Visualization with highlighted features

### Understanding Surgery Difficulty Assessment

The Surgery Difficulty Calculator provides:

1. **Difficulty Level**: Categorizes the potential surgery into one of three levels:
   - **Resident Level** (Low difficulty): Suitable for residents under supervision
   - **Specialist Level** (Medium difficulty): Requires specialist experience
   - **Consultant Level** (High difficulty): Requires consultant expertise

2. **Points Breakdown**: Shows how the difficulty score was calculated based on:
   - JRS Classification (Japanese Rhinologic Society classification type)
   - Frontal Ostium Grade (accessibility of the frontal sinus)
   - Anatomical Complexity (presence of Haller cells, skull base defects, etc.)
   - Lund-Mackay Score (extent of sinus opacification)

3. **Instrument Recommendations**: Suggests appropriate surgical instruments categorized by:
   - Endoscopes (different angles based on difficulty)
   - Forceps (standard and specialized)
   - Suction & Elevators
   - Powered Instruments (microdebriders, drills)
   - Other Equipment (navigation systems, specialized tools)

### Accessing the Admin Section

1. Navigate to the `/admin` URL
2. Enter your username and password
3. View recent analyses in the table
4. Click "View" to see detailed results for a specific analysis
5. Click "Feedback" to provide corrections to the algorithm

### Providing Feedback

1. Review the current analysis results
2. Make corrections to any of the classification systems:
   - Adjust Lund-Mackay scores for individual sinuses
   - Correct Haller cells detection (presence, location, size)
   - Update Kuros classification grade
   - Update Harshala classification type
3. Add any additional notes
4. Click "Submit Feedback" to save your corrections
5. The algorithm will learn from your feedback to improve future analyses

## Supported File Types

- Images: PNG, JPG, JPEG, GIF
- DICOM files: DCM, DICOM
- Videos: MP4, AVI, MOV

## Technical Information

- The application uses computer vision and image processing techniques to analyze CT scans
- Placeholder implementations are currently used for the classification systems
- In a production environment, these would be replaced with trained machine learning models
- The feedback system stores your corrections to improve the algorithm over time

## Privacy and Security

- All uploaded files are stored securely on the server
- Analysis results are only accessible to authorized users
- The admin section is protected by authentication
- No patient identifying information is required or stored

## Troubleshooting

- If file upload fails, check that the file type is supported
- If analysis results seem incorrect, use the admin feedback system to provide corrections
- For technical issues, refer to the deployment guide or contact technical support
