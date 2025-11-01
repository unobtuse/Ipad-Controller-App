import pyvjoy
import logging
import os

# Set up logging based on environment variable
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'
logging_level = logging.DEBUG if DEBUG_MODE else logging.WARNING
logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

def get_vjoy_device():
    try:
        vj = pyvjoy.VJoyDevice(1)
        logging.info("vJoy device initialized successfully")
        return vj
    except pyvjoy.exceptions.vJoyFailedToAcquireException:
        logging.warning("vJoy device is already in use. Buttons will not be mapped to vJoy.")
        return None
    except Exception as e:
        logging.error(f"Failed to initialize vJoy device: {e}", exc_info=True)
        return None

def map_input(command):
    logging.debug(f"Entering map_input function with command: {command}")
    vj = get_vjoy_device()
    if vj is None:
        logging.warning("Cannot map input because vJoy is not initialized.")
        return False

    button_mappings = {f"button_{i}": i for i in range(1, 26)}

    parts = command.split('_')
    logging.debug(f"Command parts: {parts}")
    if len(parts) == 3:
        button, action = f"{parts[0]}_{parts[1]}", parts[2]
        logging.debug(f"Parsed button: {button}, action: {action}")
        if button in button_mappings:
            button_id = button_mappings[button]
            try:
                if action == 'press':
                    logging.debug(f"Pressing vJoy button {button_id}")
                    vj.set_button(button_id, 1)
                    logging.debug(f"vJoy button {button_id} pressed successfully")
                elif action == 'release':
                    logging.debug(f"Releasing vJoy button {button_id}")
                    vj.set_button(button_id, 0)
                    logging.debug(f"vJoy button {button_id} released successfully")
                else:
                    logging.warning(f"Unknown action: {action}")
                    return False
                return True
            except Exception as e:
                logging.error(f"Error setting vJoy button {button_id}: {e}", exc_info=True)
                return False
            finally:
                logging.debug(f"Releasing vJoy device for button {button_id}")
                del vj
        else:
            logging.warning(f"Unknown button: {button}")
            return False
    else:
        logging.warning(f"Invalid command format: {command}")
        return False
