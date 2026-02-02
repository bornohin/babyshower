import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuration
RESPONSES_FILE = 'responses.json'
PORT = int(os.environ.get('PORT', 8080))

# Load responses from file
def load_responses():
    if os.path.exists(RESPONSES_FILE):
        try:
            with open(RESPONSES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# Save responses to file
def save_responses(responses):
    with open(RESPONSES_FILE, 'w') as f:
        json.dump(responses, f, indent=2)

# In-memory store
responses = load_responses()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/rsvp', methods=['POST'])
def submit_rsvp():
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400
        
        rsvp = {
            'name': data.get('name').strip(),
            'email': data.get('email').strip(),
            'attending': data.get('attending', False),
            'guests': int(data.get('guests', 0)),
            'dietary': data.get('dietary', '').strip(),
            'comments': data.get('comments', '').strip(),
            'timestamp': datetime.now().isoformat()
        }
        
        responses.append(rsvp)
        save_responses(responses)
        
        return jsonify({'success': True, 'message': 'RSVP received!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/responses', methods=['GET'])
def get_responses():
    # For demo/admin purposes (remove or protect in production)
    return jsonify({
        'total': len(responses),
        'attending': sum(1 for r in responses if r.get('attending')),
        'not_attending': sum(1 for r in responses if not r.get('attending')),
        'total_guests': sum(r.get('guests', 0) for r in responses),
        'responses': responses
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
