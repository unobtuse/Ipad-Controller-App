import asyncio
import websockets
import json
import logging
import multiprocessing
import subprocess
import sys
import os
from input_mapper import map_input

# Set up logging based on environment variable
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'
logging_level = logging.DEBUG if DEBUG_MODE else logging.WARNING
logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Load button configuration
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        button_config = json.load(f)
    # Verify that all buttons are present
    for i in range(1, 26):
        button_key = f"button_{i}"
        if button_key not in button_config:
            button_config[button_key] = {"name": "", "classes": "hidden-button"}
    logging.info("Configuration loaded successfully")
except FileNotFoundError:
    logging.warning("config.json not found. Creating a default configuration.")
    button_config = {f"button_{i}": {"name": "", "classes": "hidden-button"} for i in range(1, 26)}
except json.JSONDecodeError:
    logging.error("config.json is not valid JSON. Using default configuration.")
    button_config = {f"button_{i}": {"name": "", "classes": "hidden-button"} for i in range(1, 26)}
except Exception as e:
    logging.error(f"An error occurred while loading config.json: {e}")
    button_config = {f"button_{i}": {"name": "", "classes": "hidden-button"} for i in range(1, 26)}

async def handle_websocket(websocket, path):
    global button_config
    try:
        async for message in websocket:
            logging.debug(f"Received message: {message}")
            if message == 'get_config':
                await websocket.send(json.dumps(button_config))
                logging.debug("Sent configuration to client")
            elif message.startswith('save_config:'):
                try:
                    new_config = json.loads(message.split(':', 1)[1])
                    if all(f"button_{i}" in new_config for i in range(1, 26)):
                        button_config = new_config
                        with open('config.json', 'w', encoding='utf-8') as f:
                            json.dump(button_config, f, indent=4)
                        logging.info("Configuration saved successfully")
                    else:
                        logging.warning("Invalid configuration received. Not saving.")
                except json.JSONDecodeError:
                    logging.error("Received invalid JSON for configuration. Not saving.")
            else:
                logging.debug(f"Received button command: {message}")
                result = map_input(message)
                logging.debug(f"Button command result: {result}")
    except websockets.exceptions.ConnectionClosed:
        logging.info("WebSocket connection closed")
    except Exception as e:
        logging.error(f"Error in handle_websocket: {e}", exc_info=True)

async def run_websocket_server():
    try:
        server = await websockets.serve(handle_websocket, "0.0.0.0", 8765)
        logging.info("WebSocket server started on port 8765")
        await server.wait_closed()
    except OSError as e:
        if e.errno == 10048:  # Address already in use
            logging.error("WebSocket server port 8765 is already in use. Please close any other applications using this port.")
        else:
            logging.error(f"Failed to start WebSocket server: {e}")
        os._exit(1)
    except Exception as e:
        logging.error(f"Error in run_websocket_server: {e}", exc_info=True)
        os._exit(1)

def start_websocket_server():
    asyncio.run(run_websocket_server())

def run_http_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        subprocess.run([sys.executable, "-m", "http.server", "8000"])
    except Exception as e:
        logging.error(f"Failed to start HTTP server: {e}", exc_info=True)
        os._exit(1)

if __name__ == "__main__":
    if DEBUG_MODE:
        print("Running in DEBUG mode. Set DEBUG_MODE=False to disable debug output.")
    else:
        print("Running in PRODUCTION mode. Set DEBUG_MODE=True to enable debug output.")

    websocket_process = multiprocessing.Process(target=start_websocket_server)
    websocket_process.start()

    http_process = multiprocessing.Process(target=run_http_server)
    http_process.start()

    try:
        websocket_process.join()
        http_process.join()
    except KeyboardInterrupt:
        logging.info("Terminating servers...")
        websocket_process.terminate()
        http_process.terminate()
        websocket_process.join()
        http_process.join()
        logging.info("Servers terminated.")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        websocket_process.terminate()
        http_process.terminate()
        websocket_process.join()
        http_process.join()
        logging.info("Servers terminated due to an error.")
