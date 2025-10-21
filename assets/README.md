# Assets

This directory contains screenshots and visual assets for the EP-133 K.O. II Skills project.

## Current Assets

### `session-screenshot-2025-10-21.png`
Reference screenshot of the official Teenage Engineering EP Sample Tool interface used as design inspiration.

### `web-interface-preview.png` (To be added)
Screenshot of our web interface showing:
- Visual device representation with 48-pad grid
- Sample library browser
- Playback controls
- Pattern sequencer
- Connection status

## How to Capture a Preview

1. **Start the web interface:**
   ```bash
   python3 web_interface.py
   ```

2. **Open in browser:**
   - Navigate to `http://localhost:5000`
   - Click "Connect Device" (or it will show disconnected state)

3. **Take screenshot:**
   - Full window screenshot recommended
   - Capture both left (device) and right (controls) panels
   - Include the "EP SAMPLE TOOL" header

4. **Save to this directory:**
   - Filename: `web-interface-preview.png`
   - Recommended size: 1400-1600px wide
   - Format: PNG for best quality

5. **Commit:**
   ```bash
   git add assets/web-interface-preview.png
   git commit -m "Add web interface preview screenshot"
   git push
   ```

## Preview Checklist

For a good preview screenshot, make sure to show:
- [ ] Both device and controls panels visible
- [ ] Clean, uncluttered interface
- [ ] Sample library with some categories expanded
- [ ] Connection status visible
- [ ] Professional appearance matching TE aesthetic

---

*These visual assets help users understand the interface before installing.*
