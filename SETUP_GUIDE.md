# Virtual Gamepad - Detailed Setup Guide

This guide will walk you through the complete setup process for the Virtual Gamepad application.

## Table of Contents
1. [Prerequisites Installation](#prerequisites-installation)
2. [Network Configuration](#network-configuration)
3. [Application Setup](#application-setup)
4. [First-Time Configuration](#first-time-configuration)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites Installation

### 1. Install Python

**Windows:**
1. Download Python 3.7 or later from [python.org](https://www.python.org/downloads/)
2. During installation, **check the box** "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

### 2. Install vJoy Driver (Windows Only)

1. Download vJoy from [vJoy Official Site](http://vjoystick.sourceforge.net/site/)
2. Run the installer as Administrator
3. After installation, open **Configure vJoy** from the Start Menu
4. Configure Device 1:
   - Enable: **Yes**
   - Number of Buttons: **25** (or more)
   - POVs: 0 (or as needed)
   - Click **Apply**

5. Verify installation:
   - Open Windows **Game Controllers** (search "Set up USB game controllers")
   - You should see "vJoy Device" listed

---

## Network Configuration

### Finding Your PC's IP Address

**Windows:**
1. Open Command Prompt (Win + R, type `cmd`)
2. Run: `ipconfig`
3. Look for "IPv4 Address" under your active network adapter (usually `192.168.x.x`)

**macOS:**
1. Open Terminal
2. Run: `ifconfig | grep "inet "`
3. Look for your local IP (usually `192.168.x.x`)

**Linux:**
```bash
ip addr show
```

### Firewall Configuration

**Windows Firewall:**
1. Open **Windows Defender Firewall**
2. Click **Advanced Settings**
3. Click **Inbound Rules** → **New Rule**
4. Select **Port** → Next
5. Select **TCP** and enter ports: `8000, 8765`
6. Allow the connection
7. Apply to all profiles
8. Name it "Virtual Gamepad"

**Alternative (Quick but less secure):**
- Temporarily disable Windows Firewall for testing
- Settings → Windows Security → Firewall & Network Protection → Turn off

---

## Application Setup

### 1. Clone or Download the Repository

**Using Git:**
```bash
git clone https://github.com/yourusername/virtual-gamepad.git
cd virtual-gamepad
```

**Or download ZIP:**
- Download and extract the ZIP file
- Open Command Prompt/Terminal in the extracted folder

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your command prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Common Installation Issues:**

If `pyvjoy` fails to install:
```bash
pip install pyvjoy --no-cache-dir
```

If you get SSL errors:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 4. Configure WebSocket Address

1. Open `index.html` in a text editor
2. Find line ~266:
   ```javascript
   ws = new WebSocket("ws://192.168.0.33:8765");
   ```
3. Replace `192.168.0.33` with your PC's IP address
4. Save the file

---

## First-Time Configuration

### Starting the Servers

**Recommended Method (Windows):**
```bash
start_servers.bat
```

**Cross-Platform Method:**
```bash
python run_servers.py
```

**Manual Method (Two terminals):**

Terminal 1:
```bash
python server.py
```

Terminal 2:
```bash
python -m http.server 8000
```

### Expected Output

You should see:
```
Running in PRODUCTION mode. Set DEBUG_MODE=True to enable debug output.
WebSocket server started on port 8765
HTTP server started on port 8000
```

### Accessing from Your iPad/Tablet

1. **Ensure both devices are on the same Wi-Fi network**
2. Open Safari (or any browser) on your iPad
3. Navigate to: `http://YOUR_PC_IP:8000`
   - Example: `http://192.168.0.33:8000`
4. You should see a 5×5 grid of buttons

### Testing the Connection

1. Open the web interface on your iPad
2. On your PC, check `server_debug.log` for:
   ```
   New connection from ('192.168.x.x', port)
   Button configuration sent to client
   ```
3. Tap a button on your iPad
4. Check the log for:
   ```
   Received message: button_1_press
   ```

---

## First-Time Configuration

### Customizing Your Buttons

1. **Enter Edit Mode:**
   - Tap the **✏️ (pencil)** button in the top-left corner
   - The button changes to "Save Layout"

2. **Edit a Button:**
   - Tap any button to edit it
   - Change the text label
   - Select a color
   - Click "Save Button"

3. **Rearrange Buttons:**
   - In edit mode, drag and drop buttons to new positions

4. **Save Your Layout:**
   - Tap "Save Layout" when finished
   - Configuration automatically saves to `config.json`

### Testing vJoy Input

1. **Open vJoy Monitor:**
   - Search for "Monitor vJoy" in Start Menu
   - Select Device 1

2. **Test Buttons:**
   - Tap buttons on your iPad interface
   - Watch the corresponding buttons light up in vJoy Monitor

3. **Test in a Game:**
   - Open your game's controller settings
   - Look for "vJoy Device"
   - Assign buttons as needed
   - Test by tapping buttons on your iPad

---

## Troubleshooting

### "Cannot Connect to WebSocket"

**Check 1: Server Running?**
- Verify the server is running with no errors
- Check that both ports 8000 and 8765 are mentioned in the output

**Check 2: Correct IP Address?**
- Verify the IP in `index.html` matches your PC's IP
- Try accessing `http://YOUR_PC_IP:8000` from your PC's browser first

**Check 3: Same Network?**
- Ensure iPad and PC are on the same Wi-Fi network
- Check router settings don't block device-to-device communication

**Check 4: Firewall?**
- Temporarily disable firewall to test
- If it works, add firewall rules for ports 8000 and 8765

### "vJoy Device Not Found"

**Solution 1: Reinstall vJoy**
- Uninstall current vJoy
- Restart PC
- Install latest version
- Configure Device 1 with 25+ buttons

**Solution 2: Check Device Status**
- Open "Configure vJoy"
- Ensure Device 1 is Enabled
- Click Apply

**Solution 3: Check Device ID**
- In `input_mapper.py`, verify line 12:
  ```python
  vj = pyvjoy.VJoyDevice(1)  # Should be 1
  ```

### "Buttons Not Working in Game"

**Issue:** Game doesn't recognize vJoy device
- **Solution:** Some games require native controllers only (won't work)
- **Workaround:** Try different games or use additional software like JoyToKey

**Issue:** Wrong buttons mapped
- **Solution:** Check game's controller settings and remap

**Issue:** Multiple controllers interfering
- **Solution:** Disconnect other controllers temporarily

### "Port Already in Use"

**Error:** `Address already in use` for port 8765 or 8000

**Solution:**
1. Find and kill the process:
   ```bash
   # Windows:
   netstat -ano | findstr :8765
   taskkill /PID <PID> /F
   
   # Linux/macOS:
   lsof -i :8765
   kill -9 <PID>
   ```

2. Or simply restart your PC

### "Lag or Delayed Input"

**Causes:**
- Weak Wi-Fi signal
- Network congestion
- Other devices on network

**Solutions:**
- Move closer to router
- Use 5GHz Wi-Fi if available
- Close bandwidth-heavy applications
- Consider using a dedicated router/network

### "Configuration Not Saving"

**Check 1: File Permissions**
- Ensure `config.json` is not read-only
- Run the script with appropriate permissions

**Check 2: Syntax Errors**
- Check `server_debug.log` for JSON errors
- Manually verify `config.json` is valid JSON

**Check 3: WebSocket Connection**
- Configuration only saves if WebSocket is connected
- Check browser console for connection errors

---

## Advanced Configuration

### Debug Mode

Enable detailed logging:

**Windows CMD:**
```bash
set DEBUG_MODE=True
python run_servers.py
```

**Windows PowerShell:**
```powershell
$env:DEBUG_MODE="True"
python run_servers.py
```

**Linux/macOS:**
```bash
export DEBUG_MODE=True
python run_servers.py
```

### Changing Ports

**WebSocket Port (default 8765):**
- Edit `server.py`, `combined_server.py`, and `run_servers.py`
- Change all instances of `8765` to your desired port
- Update `index.html` line 266

**HTTP Port (default 8000):**
- Edit `combined_server.py` and `run_servers.py`
- Change all instances of `8000` to your desired port
- Access via `http://YOUR_PC_IP:NEW_PORT`

### Using with Multiple Devices

You can connect multiple iPads/tablets simultaneously:
1. Each device connects to the same server
2. All devices will control the same vJoy device
3. Be careful of button conflicts!

---

## Performance Tips

### For Best Latency:
1. Use 5GHz Wi-Fi (802.11ac or better)
2. Place router centrally between PC and iPad
3. Minimize network traffic during gaming
4. Close unnecessary browser tabs on iPad
5. Use a modern browser (Safari, Chrome)

### For Best Battery Life:
1. Reduce screen brightness on iPad
2. Disable auto-lock (Settings → Display & Brightness)
3. Close other apps running in background

---

## Getting Help

If you're still experiencing issues:

1. **Check Logs:**
   - `server_debug.log` - Server-side errors
   - Browser Console (F12) - Client-side errors

2. **Search Issues:**
   - Check GitHub issues for similar problems
   - Search for error messages

3. **Create an Issue:**
   - Include your OS and Python version
   - Copy relevant log excerpts
   - Describe what you tried
   - Mention if it worked before

4. **Common Error Messages:**
   - See the main README.md for common issues section

---

## Next Steps

Once everything is working:
1. Customize your button layout for your specific game
2. Create multiple config files for different games
3. Explore color coding for different button types
4. Share your configuration with others!

Happy gaming! 🎮

