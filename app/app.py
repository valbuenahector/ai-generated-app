from flask import Flask, render_template, request
import os

app = Flask(__name__)

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
