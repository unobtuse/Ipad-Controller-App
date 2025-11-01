import asyncio
import websockets
import logging
import json
import sys
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

print("Starting server.py script...")
logging.info("Starting server.py script...")

# Load button configuration
try:
    with open('config.json', 'r') as f:
        button_config = json.load(f)
    logging.info("Button configuration loaded successfully")
    print("Button configuration loaded successfully")
except Exception as e:
    logging.error(f"Failed to load button configuration: {e}")
    print(f"Failed to load button configuration: {e}")
    button_config = {}

async def handle_connection(websocket, path):
    logging.info(f"New connection from {websocket.remote_address}")
    print(f"New connection from {websocket.remote_address}")
    try:
        # Send button configuration to the client
        await websocket.send(json.dumps(button_config))
        logging.info("Button configuration sent to client")
        print("Button configuration sent to client")
        
        async for message in websocket:
            logging.info(f"Received message: {message}")
            print(f"Received message: {message}")
            map_input(message)
    except websockets.ConnectionClosed:
        logging.info(f"Connection closed from {websocket.remote_address}")
        print(f"Connection closed from {websocket.remote_address}")
    except Exception as e:
        logging.error(f"Error in handle_connection: {e}")
        print(f"Error in handle_connection: {e}")

async def main():
    logging.info("Starting WebSocket server...")
    print("Starting WebSocket server...")
    try:
        server = await websockets.serve(handle_connection, "0.0.0.0", 8765)
        logging.info("WebSocket server started on ws://0.0.0.0:8765")
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever
    except asyncio.CancelledError:
        logging.info("Server is shutting down...")
        print("Server is shutting down...")
    except Exception as e:
        logging.error(f"Failed to start WebSocket server: {e}")
        print(f"Failed to start WebSocket server: {e}")
    finally:
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    try:
        logging.info("Running main function...")
        print("Running main function...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Shutting down...")
        logging.info("KeyboardInterrupt received. Shutting down...")
    except Exception as e:
        logging.error(f"Error running main: {e}")
        print(f"Error running main: {e}")
