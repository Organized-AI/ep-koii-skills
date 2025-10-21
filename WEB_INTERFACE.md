# EP-133 K.O. II Web Interface

A modern, real-time web interface for controlling the EP-133 K.O. II device and visualizing playback.

## Features

### 🎹 Visual Pad Grid
- **4 Pad Groups** (A, B, C, D) with 12 pads each (48 total)
- Real-time visual feedback when pads are triggered
- Click any pad to play the corresponding MIDI note
- Color-coded groups for easy navigation
- Pad notation display (A1, B5, C9, etc.)

### 🎵 Sample Management
- Browse sound categories (Kicks, Snares, Cymbals, Bass, etc.)
- Search functionality for finding specific sounds
- 240+ sounds across 6 categories
- Quick access to sound library

### 🎚️ Playback Controls
- **Velocity Control**: Adjust note velocity (0-127)
- **Duration Control**: Set note duration (50-2000ms)
- Real-time parameter adjustment
- Visual indicators for current settings

### 🎼 Pattern Sequencer
- 16-step sequencer for creating patterns
- Adjustable BPM (60-200)
- Visual playback indicator showing current step
- Click pads to add them to sequence steps
- Play, stop, and clear pattern controls
- Real-time pattern playback

### 📊 Audio Visualizer
- Real-time visual feedback during playback
- Animated bars that respond to note events
- Smooth animations and transitions

### 🔌 Connection Management
- Auto-detect EP-133 K.O. II device
- Manual port selection support
- Live connection status indicator
- Connect/disconnect controls

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify your EP-133 K.O. II is connected** via USB-C

3. **Run the web interface:**
   ```bash
   python3 web_interface.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Connecting to Your Device

1. Connect your EP-133 K.O. II via USB-C
2. Click the **"Connect"** button in the interface
3. The status indicator will turn green when connected

### Playing Pads

1. Click any pad in the grid to play it
2. Adjust velocity and duration using the sliders
3. Visual feedback will show on the pad and visualizer

### Creating Patterns

1. **Select a pad** by clicking it (it will highlight)
2. **Click sequencer steps** (1-16) to add that pad to those steps
3. Adjust the **BPM** as desired
4. Click **"Play Pattern"** to start playback
5. Watch the current step highlight as it plays

### Browsing Samples

1. Use the **search box** to find specific sounds
2. Click **category names** to browse by category
3. Categories include:
   - Kicks
   - Snares
   - Cymbals and Hats
   - Percussion
   - Bass
   - Melodic & Synth

## Architecture

### Backend (Flask + SocketIO)

The web server (`web_interface.py`) provides:

- **REST API endpoints** for device control and sample management
- **WebSocket connections** for real-time bidirectional communication
- **Multi-threaded pattern playback** with precise timing
- **Integration** with the EP133Skill library

#### API Endpoints

```
GET  /                           - Main interface
GET  /api/midi/ports            - List MIDI ports
POST /api/midi/connect          - Connect to device
POST /api/midi/disconnect       - Disconnect from device
GET  /api/midi/status           - Get connection status
GET  /api/samples/categories    - List all categories
GET  /api/samples/category/:cat - Get sounds in category
POST /api/samples/search        - Search sounds
GET  /api/samples/:id           - Get sound info
```

#### WebSocket Events

**Client → Server:**
- `play_note` - Play a single note
- `play_pattern` - Start pattern playback
- `stop_pattern` - Stop pattern playback

**Server → Client:**
- `connection_status` - Connection state changed
- `note_playing` - Note started playing
- `note_stopped` - Note stopped playing
- `pattern_step` - Pattern advanced to next step
- `pattern_started` - Pattern playback began
- `pattern_stopped` - Pattern playback ended
- `error` - Error occurred

### Frontend (HTML/CSS/JavaScript)

The interface (`templates/index.html`) features:

- **Responsive grid layout** that adapts to screen size
- **Real-time WebSocket communication** via Socket.IO
- **Animated visualizations** using CSS animations
- **Dark theme** optimized for extended use
- **Touch-friendly controls** for tablets/mobile

## Technical Details

### MIDI Note Mapping

```
Group A: MIDI notes 36-47  (pads A1-A12)
Group B: MIDI notes 48-59  (pads B1-B12)
Group C: MIDI notes 60-71  (pads C1-C12)
Group D: MIDI notes 72-83  (pads D1-D12)
```

### Pattern Timing

- **16th note resolution** for patterns
- Step duration = `60 / BPM / 4` seconds
- Note duration = step duration × 0.8 (80% of step)

### Performance

- **Non-blocking I/O** via threading and async operations
- **Efficient WebSocket** communication for minimal latency
- **Optimized animations** using CSS transforms and GPU acceleration

## Troubleshooting

### "Not connected to device"
- Ensure your EP-133 K.O. II is connected via USB-C
- Check that MIDI device is detected by your OS
- Try reconnecting using the Connect button
- Run `python3 connect_koii.py` to verify MIDI connection

### Port Already in Use
```bash
# Kill any process using port 5000
sudo lsof -ti:5000 | xargs kill -9

# Or change the port in web_interface.py
socketio.run(app, host='0.0.0.0', port=8080)
```

### MIDI Device Not Found
```bash
# List available MIDI ports
python3 -c "import mido; print(mido.get_output_names())"
```

### WebSocket Connection Failed
- Check your firewall settings
- Ensure port 5000 is not blocked
- Try accessing via `127.0.0.1:5000` instead of `localhost:5000`

## Advanced Usage

### Custom Port Configuration

Edit `web_interface.py` to specify a custom MIDI port:

```python
@app.route('/api/midi/connect', methods=['POST'])
def connect():
    # Specify exact port name
    success = skill.connect_to_device(port_name="EP-133 K.O. II")
```

### Pattern Export/Import

Patterns are stored as JSON arrays. You can save/load them:

```javascript
// In browser console
const myPattern = pattern;
localStorage.setItem('pattern1', JSON.stringify(myPattern));

// Load pattern
const loadedPattern = JSON.parse(localStorage.getItem('pattern1'));
```

### Multiple Clients

The WebSocket implementation supports multiple simultaneous clients:
- All clients receive real-time playback updates
- Any client can control the device
- Pattern changes broadcast to all connected clients

## Integration with Claude Code

The web interface is designed to work seamlessly with Claude Code workflows:

1. **Visual Debugging**: See exactly which pads are triggering
2. **Pattern Development**: Iterate quickly on pattern designs
3. **Sample Exploration**: Browse and test sounds interactively
4. **Real-time Feedback**: Immediate visual confirmation of actions

## Future Enhancements

Potential additions to the interface:

- [ ] Sample upload and management
- [ ] Pattern save/load functionality
- [ ] Multiple pattern tracks
- [ ] MIDI recording and export
- [ ] Visual waveform display
- [ ] Keyboard shortcuts
- [ ] Touch gesture support
- [ ] Custom pad assignments
- [ ] Effect parameters control
- [ ] Session recording

## Contributing

To extend the web interface:

1. **Backend**: Add new API endpoints in `web_interface.py`
2. **Frontend**: Modify `templates/index.html`
3. **Styling**: Update CSS in the `<style>` section
4. **Features**: Add new WebSocket events for real-time features

## License

This web interface is part of the ep-koii-skills project and is licensed under the MIT License.

## Credits

Built with:
- Flask - Web framework
- Socket.IO - Real-time communication
- EP133Skill - MIDI control library
- Teenage Engineering - Original EP-133 K.O. II hardware

---

**Enjoy creating music with your EP-133 K.O. II!** 🎵
