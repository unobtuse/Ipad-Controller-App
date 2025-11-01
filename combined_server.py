import asyncio
import websockets
import logging
import json
import sys
import os
import psutil
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread
from input_mapper import map_input

# Configure logging to write to both console and file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server_debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Starting combined_server.py script...")

# Load button configuration
try:
    with open('config.json', 'r') as f:
        button_config = json.load(f)
    logging.info(f"Button configuration loaded successfully: {button_config}")
except Exception as e:
    logging.error(f"Failed to load button configuration: {e}")
    button_config = {}

async def handle_connection(websocket, path):
    logging.info(f"New connection from {websocket.remote_address}")
    try:
        # Send button configuration to the client
        await websocket.send(json.dumps(button_config))
        logging.info(f"Button configuration sent to client: {button_config}")
        
        async for message in websocket:
            logging.info(f"Received message: {message}")
            if message == 'get_config':
                await websocket.send(json.dumps(button_config))
                logging.info("Sent current button configuration to client")
            elif message.startswith('save_config:'):
                try:
                    new_config = json.loads(message.split(':', 1)[1])
                    button_config.update(new_config)
                    with open('config.json', 'w') as f:
                        json.dump(button_config, f, indent=4)
                    logging.info("Configuration saved successfully")
                    await websocket.send(json.dumps({"status": "success", "message": "Configuration saved"}))
                except Exception as e:
                    logging.error(f"Error saving configuration: {e}", exc_info=True)
                    await websocket.send(json.dumps({"status": "error", "message": str(e)}))
            else:
                try:
                    result = map_input(message)
                    logging.info(f"map_input result: {result}")
                except Exception as e:
                    logging.error(f"Error in map_input: {e}", exc_info=True)
    except websockets.ConnectionClosed:
        logging.info(f"Connection closed from {websocket.remote_address}")
    except Exception as e:
        logging.error(f"Error in handle_connection: {e}", exc_info=True)

async def start_websocket_server():
    logging.info("Starting WebSocket server...")
    try:
        server = await websockets.serve(handle_connection, "0.0.0.0", 8765)
        logging.info("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever
    except asyncio.CancelledError:
        logging.info("Server is shutting down...")
    except Exception as e:
        logging.error(f"Failed to start WebSocket server: {e}", exc_info=True)
    finally:
        server.close()
        await server.wait_closed()

def start_http_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    logging.info("HTTP server started on http://0.0.0.0:8000")
    httpd.serve_forever()

def monitor_memory():
    process = psutil.Process(os.getpid())
    while True:
        mem_info = process.memory_info()
        logging.info(f"Memory usage: {mem_info.rss / (1024 * 1024):.2f} MB")
        time.sleep(60)  # Log memory usage every 60 seconds

def main():
    logging.info("Starting main function...")
    # Start HTTP server in a separate thread
    http_thread = Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()
    logging.info("HTTP server thread started")

    # Start memory monitoring in a separate thread
    memory_thread = Thread(target=monitor_memory)
    memory_thread.daemon = True
    memory_thread.start()
    logging.info("Memory monitoring thread started")

    # Start WebSocket server
    logging.info("Starting WebSocket server in main thread")
    asyncio.run(start_websocket_server())

if __name__ == "__main__":
    try:
        logging.info("Running main function...")
        main()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Shutting down...")
    except Exception as e:
        logging.error(f"Error running main: {e}", exc_info=True)
