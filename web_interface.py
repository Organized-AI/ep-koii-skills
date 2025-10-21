#!/usr/bin/env python3
"""
Web Interface for EP-133 K.O. II Skills
Provides a visual interface for controlling the device and visualizing playback.
"""

import json
import time
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from ep_koii_skills import EP133Skill
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ep-koii-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global skill instance
skill = EP133Skill()
connected = False
current_pattern = []
is_playing = False

# Pad group definitions
PAD_GROUPS = {
    'A': list(range(36, 48)),  # A1-A12
    'B': list(range(48, 60)),  # B1-B12
    'C': list(range(60, 72)),  # C1-C12
    'D': list(range(72, 84))   # D1-D12
}

@app.route('/')
def index():
    """Serve the main interface"""
    return render_template('index.html')

@app.route('/api/midi/ports', methods=['GET'])
def list_ports():
    """List available MIDI ports"""
    try:
        ports = skill.list_midi_ports()
        return jsonify({'success': True, 'ports': ports})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/midi/connect', methods=['POST'])
def connect():
    """Connect to MIDI device"""
    global connected
    try:
        data = request.json
        port_name = data.get('port_name') if data else None

        success = skill.connect_to_device(port_name=port_name)
        connected = success

        if success:
            socketio.emit('connection_status', {'connected': True})
            return jsonify({'success': True, 'message': 'Connected successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to connect'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/midi/disconnect', methods=['POST'])
def disconnect():
    """Disconnect from MIDI device"""
    global connected
    try:
        skill.disconnect_device()
        connected = False
        socketio.emit('connection_status', {'connected': False})
        return jsonify({'success': True, 'message': 'Disconnected successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/midi/status', methods=['GET'])
def status():
    """Get connection status"""
    return jsonify({'connected': skill.is_connected()})

@app.route('/api/samples/categories', methods=['GET'])
def get_categories():
    """Get all sound categories"""
    try:
        categories = skill.list_sound_categories()
        return jsonify({'success': True, 'categories': categories})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/samples/category/<category>', methods=['GET'])
def get_sounds_in_category(category):
    """Get sounds in a specific category"""
    try:
        sounds = skill.list_sounds_in_category(category)
        return jsonify({'success': True, 'sounds': sounds})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/samples/search', methods=['POST'])
def search_sounds():
    """Search for sounds"""
    try:
        data = request.json
        query = data.get('query', '')
        results = skill.search_sounds(query)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/samples/<int:sound_id>', methods=['GET'])
def get_sound_info(sound_id):
    """Get information about a specific sound"""
    try:
        info = skill.get_sound_info(sound_id)
        if info:
            return jsonify({'success': True, 'info': info})
        else:
            return jsonify({'success': False, 'error': 'Sound not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@socketio.on('play_note')
def handle_play_note(data):
    """Handle note play request via WebSocket"""
    try:
        note = data.get('note')
        velocity = data.get('velocity', 100)
        duration = data.get('duration', 0.1)
        pad_id = data.get('pad_id', '')

        if not connected:
            emit('error', {'message': 'Not connected to device'})
            return

        # Emit playback start event
        emit('note_playing', {
            'note': note,
            'pad_id': pad_id,
            'velocity': velocity
        }, broadcast=True)

        # Play the note
        skill.play_note(note, velocity=velocity, duration=duration)

        # Schedule playback end event
        def emit_note_off():
            time.sleep(duration)
            socketio.emit('note_stopped', {
                'note': note,
                'pad_id': pad_id
            }, broadcast=True)

        threading.Thread(target=emit_note_off, daemon=True).start()

    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('play_pattern')
def handle_play_pattern(data):
    """Handle pattern play request via WebSocket"""
    global is_playing

    try:
        pattern = data.get('pattern', [])
        bpm = data.get('bpm', 120)
        loop = data.get('loop', False)

        if not connected:
            emit('error', {'message': 'Not connected to device'})
            return

        if is_playing:
            emit('error', {'message': 'Pattern already playing'})
            return

        def play_pattern_thread():
            global is_playing
            is_playing = True
            step_duration = 60.0 / bpm / 4  # 16th note duration

            try:
                while is_playing:
                    for step_idx, step in enumerate(pattern):
                        if not is_playing:
                            break

                        # Emit step event
                        socketio.emit('pattern_step', {
                            'step': step_idx,
                            'total_steps': len(pattern)
                        }, broadcast=True)

                        # Play notes in this step
                        for note_data in step:
                            note = note_data.get('note')
                            velocity = note_data.get('velocity', 100)
                            pad_id = note_data.get('pad_id', '')

                            socketio.emit('note_playing', {
                                'note': note,
                                'pad_id': pad_id,
                                'velocity': velocity,
                                'step': step_idx
                            }, broadcast=True)

                            skill.play_note(note, velocity=velocity, duration=step_duration * 0.8)

                        time.sleep(step_duration)

                    if not loop:
                        break

            finally:
                is_playing = False
                socketio.emit('pattern_stopped', {}, broadcast=True)

        threading.Thread(target=play_pattern_thread, daemon=True).start()
        emit('pattern_started', {'success': True})

    except Exception as e:
        is_playing = False
        emit('error', {'message': str(e)})

@socketio.on('stop_pattern')
def handle_stop_pattern():
    """Stop pattern playback"""
    global is_playing
    is_playing = False
    emit('pattern_stopped', {}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connection_status', {'connected': connected})

if __name__ == '__main__':
    print("Starting EP-133 K.O. II Web Interface...")
    print("Access the interface at: http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
