import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CT Scan Analysis Website</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                color: #333;
                background-color: #f5f5f5;
            }
            .container {
                width: 80%;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            header {
                background-color: #3a6ea5;
                color: white;
                text-align: center;
                padding: 1rem;
                margin-bottom: 2rem;
            }
            h1 {
                margin: 0;
            }
            .card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin-bottom: 20px;
            }
            .feature {
                margin-bottom: 10px;
                padding-left: 20px;
                position: relative;
            }
            .feature:before {
                content: "✓";
                position: absolute;
                left: 0;
                color: #3a6ea5;
            }
            footer {
                text-align: center;
                margin-top: 2rem;
                padding: 1rem;
                background-color: #f0f0f0;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>CT Scan Analysis Website</h1>
        </header>
        
        <div class="container">
            <div class="card">
                <h2>Welcome to Our Service</h2>
                <p>Our CT scan analysis website provides advanced analysis of CT scans for ENT specialists, with a focus on sinus procedures.</p>
                
                <h3>Features:</h3>
                <div class="feature">Lund-Mackay scoring system for sinus opacification</div>
                <div class="feature">Haller cells detection</div>
                <div class="feature">Kuros classification</div>
                <div class="feature">Skull base defect detection</div>
                <div class="feature">Surgery difficulty calculator with instrument recommendations</div>
            </div>
            
            <div class="card">
                <h2>Surgery Difficulty Calculator</h2>
                <p>Our surgery difficulty calculator categorizes sinus procedures into three levels:</p>
                <ul>
                    <li><strong>Resident Level</strong> - Low difficulty procedures suitable for residents</li>
                    <li><strong>Specialist Level</strong> - Medium difficulty procedures requiring specialist expertise</li>
                    <li><strong>Consultant Level</strong> - High difficulty procedures requiring consultant-level experience</li>
                </ul>
                <p>The calculator also recommends appropriate surgical instruments based on the calculated difficulty level.</p>
            </div>
        </div>
        
        <footer>
            <p>© 2025 CT Scan Analysis Website. All rights reserved.</p>
        </footer>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
