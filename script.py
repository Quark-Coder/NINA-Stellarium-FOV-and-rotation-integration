import os
import json
import asyncio
import aiohttp
import traceback
import requests

from pynput import keyboard
from colorama import Fore, just_fix_windows_console

just_fix_windows_console()

STELLARIUM_API_URL = "http://localhost:8090/api/scripts/direct"
NINA_ADVANCED_API_URL = "http://localhost:1888/v2/api/equipment/rotator/info"
CONFIG_FILE = "config.json"

running = True
prev_angle = None


def load_config():
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                print(Fore.LIGHTBLUE_EX + "Config file found. You can change parameters in config.json." + Fore.RESET)
                return config
        except Exception as e:
            print(Fore.RED + "Error reading config file, starting fresh:" + Fore.RESET, e)
    return {}


def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(Fore.RED + "Error saving config file:" + Fore.RESET, e)


def send_stellarium_command(command):
    payload = {"code": command}
    try:
        response = requests.post(STELLARIUM_API_URL, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(Fore.RED + "Stellarium is not running. Please start Stellarium and try again." + Fore.RESET)
        input("Press Enter to exit...")
        exit(1)


async def get_nina_angle():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(NINA_ADVANCED_API_URL) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("Response", {}).get("Position", None)
        except Exception as e:
            print(Fore.RED + f"NINA connection error: {e}" + Fore.RESET)
            return None


def on_press(key):
    global running
    try:
        if key.char.lower() == 'f':
            send_stellarium_command(f"TelescopeControl.centeringScreenByTelescope({telescopeControlSlot});")
            print(Fore.LIGHTGREEN_EX + "F key pressed -> Centering telescope." + Fore.RESET)
    except AttributeError:
        if key == keyboard.Key.esc:
            print(Fore.YELLOW + "ESC pressed, exiting script..." + Fore.RESET)
            running = False
            return False
    except Exception as e:
        print(Fore.RED + f"Error during key press: {e}" + Fore.RESET)


async def update_angle():
    global prev_angle
    while running:
        angle = await get_nina_angle()
        if angle is not None and angle != prev_angle:
            send_stellarium_command(f"Oculars.setSelectedCCDRotationAngle({360-angle})")
            prev_angle = angle
        await asyncio.sleep(0.2)


if __name__ == "__main__":
    try:
        print(Fore.BLUE + "Author: Quark-Coder" + Fore.RESET)
        print(
            Fore.BLUE + "This script allows you to transfer FOV and camera rotation directly to Stellarium in real time." + Fore.RESET)

        config = load_config()

        telescopeControlSlot = config.get("telescopeControlSlot") or input(
            Fore.CYAN + "[Telescope Control] Enter telescope slot: " + Fore.RESET)
        ocularsCameraIndex = config.get("ocularsCameraIndex") or input(
            Fore.CYAN + "[Oculars] Enter camera index: " + Fore.RESET)
        ocularsTelescopeIndex = config.get("ocularsTelescopeIndex") or input(
            Fore.CYAN + "[Oculars] Enter telescope index: " + Fore.RESET)

        config["telescopeControlSlot"] = telescopeControlSlot
        config["ocularsCameraIndex"] = ocularsCameraIndex
        config["ocularsTelescopeIndex"] = ocularsTelescopeIndex
        save_config(config)

        angle = asyncio.run(get_nina_angle())
        if angle is None:
            print(Fore.RED + "NINA is not running. Please start NINA and try again." + Fore.RESET)
            input("Press Enter to exit...")
            exit(1)

        send_stellarium_command(f"Oculars.selectCCDAtIndex({ocularsCameraIndex});")
        send_stellarium_command(f"Oculars.selectTelescopeAtIndex({ocularsTelescopeIndex});")
        send_stellarium_command("Oculars.toggleCCD();")
        send_stellarium_command(f"TelescopeControl.centeringScreenByTelescope({telescopeControlSlot});")

        print(Fore.GREEN + "Data sync started. Press 'F' to recenter camera. ESC to stop." + Fore.RESET)

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        asyncio.run(update_angle())

        send_stellarium_command("core.selectObjectByName(\"\", true);")
        send_stellarium_command("Oculars.toggleCCD();")

    except Exception as e:
        tb = traceback.format_exc()
        with open("error.txt", "w") as error_file:
            error_file.write(tb)
        print(e)
        input("Press Enter to exit...")


