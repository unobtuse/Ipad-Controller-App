# Virtual Gamepad - Web-Based Controller

A customizable, web-based virtual gamepad that turns your iPad, tablet, or any device with a web browser into a wireless game controller. Perfect for flight simulators, racing games, or any application that supports joystick input.

## 🎮 Features

- **25 Customizable Buttons**: Configure a 5×5 grid of buttons with custom labels and colors
- **Real-Time Input**: Low-latency WebSocket communication for instant button response
- **Touch-Optimized**: Designed specifically for iPad and touch devices with visual feedback
- **Drag & Drop Editor**: Easily rearrange buttons and customize the layout
- **8 Color Themes**: Red, Blue, Green, Yellow, Orange, Purple, White, and Gray/Hidden
- **vJoy Integration**: Maps button presses to virtual joystick inputs on Windows
- **Live Configuration**: Edit button labels, colors, and positions without restarting
- **Persistent Settings**: Button configuration automatically saves to `config.json`

## 📋 Prerequisites

### Software Requirements

1. **Python 3.7+** - [Download Python](https://www.python.org/downloads/)
2. **vJoy Driver** - [Download vJoy](http://vjoystick.sourceforge.net/site/)
   - Required for virtual joystick functionality on Windows
   - Install and configure at least one vJoy device

### Hardware Requirements

- Windows PC (for vJoy support)
- iPad, tablet, or any device with a modern web browser
- Both devices must be on the same network

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/unobtuse/Ipad-Controller-App.git
   cd Ipad-Controller-App
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Edit the WebSocket URL** in `index.html` (line 266):
   ```javascript
   ws = new WebSocket("ws://YOUR_PC_IP_ADDRESS:8765");
   ```
   Replace `YOUR_PC_IP_ADDRESS` with your computer's local IP address (e.g., `192.168.0.33`)

2. **Find your PC's IP address**:
   - Windows: Run `ipconfig` in Command Prompt
   - Look for "IPv4 Address" under your active network adapter

### Running the Application

**Option 1: Using the batch file (Windows)**
```bash
start_servers.bat
```

**Option 2: Using Python directly**
```bash
python run_servers.py
```

**Option 3: Running servers separately**
```bash
# Terminal 1 - WebSocket Server
python server.py

# Terminal 2 - HTTP Server
python -m http.server 8000
```

**Option 4: Combined server**
```bash
python combined_server.py
```

## 📱 Usage

1. **Start the servers** on your PC using one of the methods above
2. **Open your web browser** on your iPad/tablet
3. **Navigate to** `http://YOUR_PC_IP_ADDRESS:8000`
4. **Tap the edit button** (✏️) in the top-left corner to enter edit mode
5. **Customize your layout**:
   - Click/tap buttons to edit their text and color
   - Drag and drop buttons to rearrange them
   - Click "Save Layout" when done
6. **Use the gamepad**: Tap buttons to send inputs to your PC

## 🎨 Button Customization

### Available Colors
- **Red**: `red-button`
- **Blue**: `blue-button`
- **Green**: `green-button`
- **Yellow**: `yellow-button`
- **Orange**: `orange-button`
- **Purple**: `purple-button`
- **White**: `white-button`
- **Gray/Hidden**: `gray-button` or `hidden-button` (for disabled/invisible buttons)

### Manual Configuration

Edit `config.json` to manually configure buttons:

```json
{
    "button_1": {
        "name": "Button Label",
        "classes": "red-button",
        "position": 1
    }
}
```

## 🔧 Technical Architecture

### Backend Components

#### `server.py`
- WebSocket server running on port 8765
- Handles client connections and button press/release events
- Loads and sends button configuration to clients

#### `combined_server.py`
- Unified server that runs both HTTP and WebSocket servers
- Includes memory monitoring
- Supports configuration saving from the web interface

#### `run_servers.py`
- Production-ready server launcher
- Runs HTTP and WebSocket servers in separate processes
- Includes graceful shutdown handling

#### `input_mapper.py`
- Maps button commands to vJoy inputs
- Handles button press/release events
- Button mapping: `button_1` through `button_25` → vJoy buttons 1-25

#### `config.json`
- Stores button configuration (labels, colors, positions)
- Automatically updated when changes are made in edit mode

### Frontend Components

#### `index.html`
- Responsive 5×5 button grid
- WebSocket client for real-time communication
- Drag-and-drop editor interface
- Touch-optimized with visual feedback animations
- Built with vanilla JavaScript (no dependencies)

## 📡 Communication Protocol

### WebSocket Messages

**Client → Server:**
- `get_config` - Request current button configuration
- `button_X_press` - Button X pressed (X = 1-25)
- `button_X_release` - Button X released (X = 1-25)
- `save_config:{json}` - Save new configuration

**Server → Client:**
- `{json}` - Button configuration object

## 🐛 Debugging

### Enable Debug Mode

Set the `DEBUG_MODE` environment variable:

```bash
# Windows Command Prompt
set DEBUG_MODE=True
python run_servers.py

# Windows PowerShell
$env:DEBUG_MODE="True"
python run_servers.py

# Linux/macOS
export DEBUG_MODE=True
python run_servers.py
```

### Log Files
- `server_debug.log` - Detailed server logs
- `error.log` - Error messages and exceptions

### Common Issues

**Issue**: WebSocket connection fails
- **Solution**: Check that your firewall allows connections on port 8765
- **Solution**: Verify you're using the correct IP address in `index.html`

**Issue**: Buttons don't work
- **Solution**: Ensure vJoy is installed and at least one device is configured
- **Solution**: Check `server_debug.log` for error messages

**Issue**: Can't connect from iPad
- **Solution**: Ensure both devices are on the same network
- **Solution**: Try disabling your PC's firewall temporarily to test

## 📁 Project Structure

```
virtual-gamepad/
├── server.py              # Basic WebSocket server
├── combined_server.py     # Combined HTTP + WebSocket server
├── run_servers.py         # Production server launcher
├── input_mapper.py        # vJoy input mapping
├── index.html             # Web interface
├── config.json            # Button configuration
├── requirements.txt       # Python dependencies
├── start_servers.bat      # Windows batch launcher
└── README.md             # This file
```

## 🛠️ Development

### Adding More Buttons

To add more buttons, modify:

1. **Grid layout** in `index.html` (line 26):
   ```css
   grid-template-columns: repeat(5, 1fr); /* Change 5 to desired columns */
   ```

2. **Button configuration** in `config.json`:
   ```json
   "button_26": {
       "name": "New Button",
       "classes": "blue-button",
       "position": 26
   }
   ```

3. **Button mappings** in `input_mapper.py` (line 29):
   ```python
   button_mappings = {f"button_{i}": i for i in range(1, 27)}  # Change 26 to 27
   ```

### Customizing Styles

Edit the `<style>` section in `index.html` to:
- Change button sizes
- Modify colors
- Adjust animations
- Update fonts

## 📦 Dependencies

### Python Packages
- `websockets` - WebSocket protocol implementation
- `pyvjoy` - Python interface for vJoy virtual joystick
- `psutil` - System monitoring (used in combined_server.py)

### System Requirements
- **vJoy Driver** - Virtual joystick driver for Windows

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- vJoy - Virtual joystick driver
- Bebas Neue - Font used in the interface

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Common Issues](#common-issues) section
2. Review the log files (`server_debug.log`, `error.log`)
3. Open an issue on GitHub

## 🎯 Use Cases

This virtual gamepad is perfect for:
- **Flight Simulators** (DCS, FSX, X-Plane, MSFS)
- **Racing Games** (Assetto Corsa, iRacing, BeamNG)
- **Space Simulators** (Elite Dangerous, Star Citizen)
- **Any game or application** that supports joystick input

---

**Made with ❤️ for gamers who want more buttons!**
