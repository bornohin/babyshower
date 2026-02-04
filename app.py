import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
from google.cloud import firestore

app = Flask(__name__)

# Initialize Firestore client
db = firestore.Client()
rsvps_ref = db.collection('rsvps')

PORT = int(os.environ.get('PORT', 8080))

def get_all_responses():
    """Gets all responses from the 'rsvps' collection."""
    responses = []
    for doc in rsvps_ref.stream():
        responses.append(doc.to_dict())
    return responses

@app.route('/')
def index():
    return render_template('intro.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/rsvp')
def rsvp_form():
    return render_template('rsvp.html')

@app.route('/my-rsvp')
def my_rsvp():
    return render_template('my-rsvp.html')

@app.route('/splash')
def splash():
    attending = request.args.get('attending', 'yes').lower() == 'yes'
    return render_template('splash.html', attending=attending)

@app.route('/api/rsvp', methods=['POST'])
def submit_rsvp():
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400
        
        email = data.get('email').strip().lower()
        
        # Validate number fields
        try:
            adults = int(data.get('adults', 0))
            kids = int(data.get('kids', 0))
            
            if adults < 0 or kids < 0:
                return jsonify({'error': 'Number of guests cannot be negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid number of guests'}), 400
        
        rsvp = {
            'name': data.get('name').strip(),
            'email': email,
            'attending': data.get('attending', False),
            'adults': adults,
            'kids': kids,
            'dietary': data.get('dietary', '').strip(),
            'comments': data.get('comments', '').strip(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Use email as the document ID
        rsvps_ref.document(email).set(rsvp)
        
        return jsonify({'success': True, 'message': 'RSVP received/updated!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rsvp/<email>', methods=['GET'])
def get_rsvp(email):
    try:
        email_lower = email.strip().lower()
        doc = rsvps_ref.document(email_lower).get()
        if doc.exists:
            return jsonify({'found': True, 'rsvp': doc.to_dict()}), 200
        return jsonify({'found': False, 'message': 'No RSVP found for this email'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rsvp/<email>', methods=['DELETE'])
def withdraw_rsvp(email):
    try:
        email_lower = email.strip().lower()
        rsvps_ref.document(email_lower).delete()
        return jsonify({'success': True, 'message': 'RSVP withdrawn'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/responses', methods=['GET'])
def get_responses():
    responses = get_all_responses()
    return jsonify({
        'total': len(responses),
        'attending': sum(1 for r in responses if r.get('attending')),
        'not_attending': sum(1 for r in responses if not r.get('attending')),
        'total_guests': sum(r.get('adults', 0) + r.get('kids', 0) for r in responses),
        'responses': responses
    })

@app.route('/dashboard')
def dashboard():
    responses = get_all_responses()
    stats = {
        'total': len(responses),
        'attending': sum(1 for r in responses if r.get('attending')),
        'not_attending': sum(1 for r in responses if not r.get('attending')),
        'total_adults': sum(r.get('adults', 0) for r in responses),
        'total_kids': sum(r.get('kids', 0) for r in responses),
        'total_guests': sum(r.get('adults', 0) + r.get('kids', 0) for r in responses),
        'responses': responses
    }
    return render_template('dashboard.html', stats=stats)

@app.route('/api/calendar')
def get_calendar_event():
    """Generate iCalendar (.ics) file for the Baby Shower event"""
    try:
        # Helper function to fold long lines per RFC 5545 (max 75 chars)
        def fold_line(line):
            """Fold long iCalendar lines to 75 character limit"""
            if len(line) <= 75:
                return line
            folded = []
            folded.append(line[:75])
            remainder = line[75:]
            while len(remainder) > 0:
                folded.append(' ' + remainder[:74])
                remainder = remainder[74:]
            return '\r\n'.join(folded)
        
        # Event details
        event_title = "Tiffany's Baby Shower - Dua & Celebration"
        event_date = "20260215"  # February 15, 2026
        event_time = "130000"    # 1:00 PM
        event_location = "209 James River Drive, Hutto, TX 78634"
        event_description = "Join us for a beautiful celebration of the Baby Shaad (shower) tradition!\\nDua and blessings for the mother and baby."
        
        # Create unique event ID (using timestamp)
        now = datetime.now()
        event_uid = f"baby-shower-2026@babyshower-rsvp"
        
        # Build iCalendar content with proper line folding
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Baby Shower RSVP//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:Baby Shower",
            "X-WR-TIMEZONE:America/Chicago",
            "X-WR-CALDESC:Join us for the Baby Shower celebration",
            "BEGIN:VEVENT",
            f"UID:{event_uid}",
            f"DTSTAMP:{now.strftime('%Y%m%dT%H%M%SZ')}",
            "DTSTART:20260215T130000",
            "DTEND:20260215T170000",
            f"SUMMARY:{event_title}",
            f"LOCATION:{event_location}",
            f"DESCRIPTION:{event_description}",
            "URL:https://babyshower.deviantbd.com",
            "STATUS:CONFIRMED",
            "SEQUENCE:0",
            "END:VEVENT",
            "END:VCALENDAR"
        ]
        
        # Apply line folding to each line and join with proper line endings
        ics_content = '\r\n'.join(fold_line(line) for line in lines)
        
        # Create file-like object
        ics_file = BytesIO(ics_content.encode('utf-8'))
        
        return send_file(
            ics_file,
            mimetype='text/calendar',
            as_attachment=True,
            download_name='Baby-Shower-2026.ics'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
