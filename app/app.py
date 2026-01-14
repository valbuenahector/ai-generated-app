from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'appworld-2026-secret-key')

# Module 3: Demo form submissions stored in memory
contact_submissions = []

def load_users():
    """Load users from flat file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'users.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def get_vibe_content(topic):
    """Utility to parse docs/Vibe-Coding.txt and return content for a topic."""
    # Adjusted path for local development vs container structure
    # If app.py is in /app/app.py, then docs is at /docs/Vibe-Coding.txt
    # So from app/app.py, it's ../docs/Vibe-Coding.txt
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'docs', 'Vibe-Coding.txt')
    
    # Debug: print the path being tried
    # print(f"DEBUG: Looking for file at {file_path}")
    
    try:
        # Using errors='replace' to handle potential non-UTF-8 characters in the lab doc
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        if topic == 'definition':
            # Extract Definition and History section
            start = content.find("Definition and History")
            end = content.find("Benefits of Vibe Coding")
            if start != -1 and end != -1:
                return content[start:end].strip()
        elif topic == 'ai-assisted':
            # Extract something related to AI assisted coding or tools
            start = content.find("Popular Tools and Platforms for Vibe Coding")
            end = content.find("Best Practices for Safe and Effective Vibe Coding")
            if start != -1 and end != -1:
                return content[start:end].strip()
    except Exception as e:
        # print(f"DEBUG: Error reading file: {e}")
        pass
    
    return "AI-generated synthesis (no direct quote)."

# Intentional security weakness: Debug mode enabled for "lab-only visibility"
# In a real app, this would be False in production.
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'

@app.route('/')
def home():
    """Home page: Overview of the Vibe Coding experiment."""
    return render_template('home.html')

@app.route('/about')
def about():
    """About page: Why this application exists for AppWorld 2026."""
    return render_template('about.html')

@app.route('/docs')
def docs():
    """Docs page: Educational content on Vibe Coding with citations."""
    return render_template('docs.html')

@app.route('/healthz')
def healthz():
    """Simple health endpoint returning 200, plain text."""
    return "OK", 200

@app.route('/api/status')
def api_status():
    """Module 3: API Status endpoint."""
    return jsonify({
        "status": "active",
        "version": "v0.2",
        "module": "Module 3 - API Discovery",
        "description": "Lab application for AppWorld 2026"
    })

@app.route('/api/vibe-coding')
def api_vibe_coding():
    """Module 3: Get Vibe Coding definition."""
    content = get_vibe_content('definition')
    return jsonify({
        "topic": "Vibe Coding Definition",
        "content": content,
        "source": "docs/Vibe-Coding.txt" if "AI-generated" not in content else "None"
    })

@app.route('/api/ai-assisted-coding')
def api_ai_assisted_coding():
    """Module 3: Get AI-assisted coding tools/info."""
    content = get_vibe_content('ai-assisted')
    return jsonify({
        "topic": "AI-Assisted Coding Tools",
        "content": content,
        "source": "docs/Vibe-Coding.txt" if "AI-generated" not in content else "None"
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page: Demo-only authentication."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = load_users()
        
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            return redirect(url_for('home'))
        
        return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout endpoint."""
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page: Demo form handling."""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Simple server-side validation
        if not first_name or not last_name or not email:
            return render_template('contact.html', error="Please fill in all required fields")
        
        # In-memory storage and logging
        submission = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "message": message
        }
        contact_submissions.append(submission)
        print(f"CONTACT SUBMISSION: {submission}")
        
        return render_template('contact.html', success=True, first_name=first_name)
    
    return render_template('contact.html')

# Intentional security weakness: Verbose error handling for demo
@app.errorhandler(404)
def page_not_found(e):
    # This might leak internal info in a real scenario
    return render_template('404.html', error=str(e)), 404

if __name__ == '__main__':
    # Binding to 0.0.0.0 for container compatibility
    # Using port 5001 for local host testing as requested in prompt instructions
    # (Container still exposes 5000 internally)
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
