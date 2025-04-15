import os
import json
import uuid
import cv2
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.utils import secure_filename

# Import models
from models.lund_mackay import analyze_lund_mackay
from models.haller_detector import detect_haller_cells
from models.kuros import analyze_kuros
from models.skull_base import detect_skull_base_defect
from models.feedback import save_analysis, save_feedback, get_all_analyses
from models.surgery_calculator.integration import calculate_surgery_difficulty

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ct_scan_analysis_secret_key')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff', 'dcm'}
RESULTS_FOLDER = 'static/images/results'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Admin credentials
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'ct_admin_2025')

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs('data/feedback', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image
        try:
            # Read the image
            image = cv2.imread(filepath)
            if image is None:
                return jsonify({'error': 'Could not read image file'}), 400
            
            # Analyze with different methods
            lund_mackay_results = analyze_lund_mackay(image)
            haller_results = detect_haller_cells(image)
            kuros_results = analyze_kuros(image)
            skull_base_results = detect_skull_base_defect(image)
            
            # Create result image with markers
            result_image = image.copy()
            
            # Add markers for Lund-Mackay
            cv2.putText(result_image, f"Lund-Mackay Score: {lund_mackay_results['total_score']}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Add markers for Haller cells if detected
            if haller_results['detected']:
                for cell in haller_results['locations']:
                    x, y, w, h = cell
                    cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(result_image, "Haller Cell", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            
            # Add markers for Kuros classification
            cv2.putText(result_image, f"Kuros Grade: {kuros_results['grade']}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add markers for Skull Base Defect detection
            if skull_base_results['defect_detected']:
                for defect in skull_base_results['locations']:
                    x, y, w, h = defect
                    cv2.rectangle(result_image, (x, y), (x+w, y+h), (255, 0, 255), 2)
                    cv2.putText(result_image, "Skull Base Defect", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
            
            # Save result image
            result_filename = f"result_{filename}"
            result_filepath = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
            cv2.imwrite(result_filepath, result_image)
            
            # Calculate surgery difficulty
            surgery_difficulty_results = calculate_surgery_difficulty({
                'lund_mackay': lund_mackay_results,
                'haller_cells': haller_results,
                'kuros': kuros_results,
                'skull_base': skull_base_results
            })
            
            # Prepare results
            results = {
                'original_image': filename,
                'result_image': result_filename,
                'lund_mackay': lund_mackay_results,
                'haller_cells': haller_results,
                'kuros': kuros_results,
                'skull_base': skull_base_results,
                'surgery_difficulty': surgery_difficulty_results,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save analysis for feedback
            analysis_id = save_analysis(results)
            
            return jsonify({
                'success': True,
                'results': results,
                'result_image_url': url_for('static', filename=f'images/results/{result_filename}'),
                'analysis_id': analysis_id
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/admin/analyses', methods=['GET'])
def get_analyses():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    analyses = get_all_analyses()
    return jsonify({'analyses': analyses})

@app.route('/admin/feedback', methods=['POST'])
def submit_feedback():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    analysis_id = data.get('analysis_id')
    feedback = data.get('feedback')
    
    if not analysis_id or not feedback:
        return jsonify({'error': 'Missing required fields'}), 400
    
    save_feedback(analysis_id, feedback)
    return jsonify({'success': True})

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
